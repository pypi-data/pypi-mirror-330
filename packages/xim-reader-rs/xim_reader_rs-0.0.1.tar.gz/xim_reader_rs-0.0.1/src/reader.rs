use byteorder::ByteOrder;

use binrw::{
    BinRead, args, binread,
    io::{BufReader, Read, Seek},
};

use numpy::PyArray2;
use numpy::PyArrayMethods;
use pyo3::{IntoPyObject, PyResult, prelude::Bound, pyclass, pymethods};
use pyo3_stub_gen::derive::{gen_stub_pyclass, gen_stub_pymethods};
use pyo3_stub_gen::impl_stub_type;
use std::collections::HashMap;
use std::fmt::Debug;
use std::{fs::File, path::PathBuf};

use crate::error::{Error, Result};
use byteorder::{LE, ReadBytesExt};

fn read_i32_as_usize(mut reader: impl Read, err: Error) -> Result<usize> {
    let val = reader.read_i32::<LE>()?;
    usize::try_from(val).map_err(|_err| err)
}

trait ReadFromReader<I> {
    fn read_type_into<B: ByteOrder>(&mut self, dst: &mut [I]) -> Result<()>;
}

impl<R: ReadBytesExt> ReadFromReader<i8> for R {
    fn read_type_into<B: ByteOrder>(&mut self, dst: &mut [i8]) -> Result<()> {
        Ok(self.read_i8_into(dst)?)
    }
}

impl<R: ReadBytesExt> ReadFromReader<i16> for R {
    fn read_type_into<B: ByteOrder>(&mut self, dst: &mut [i16]) -> Result<()> {
        Ok(self.read_i16_into::<B>(dst)?)
    }
}

impl<R: ReadBytesExt> ReadFromReader<i32> for R {
    fn read_type_into<B: ByteOrder>(&mut self, dst: &mut [i32]) -> Result<()> {
        Ok(self.read_i32_into::<B>(dst)?)
    }
}

impl<R: ReadBytesExt> ReadFromReader<i64> for R {
    fn read_type_into<B: ByteOrder>(&mut self, dst: &mut [i64]) -> Result<()> {
        Ok(self.read_i64_into::<B>(dst)?)
    }
}

fn parse_lookup(width: usize, height: usize) -> impl Fn(Vec<u8>) -> Vec<u8> {
    move |lookup_table: Vec<u8>| -> Vec<u8> {
        let num_bytes_table = lookup_table
            .into_iter()
            .flat_map(|vals| {
                vec![
                    (vals & 0b00000011),
                    (vals & 0b00001100) >> 2,
                    (vals & 0b00110000) >> 4,
                    (vals & 0b11000000) >> 6,
                ]
            })
            .map(|val| 1u8 << val)
            .collect::<Vec<u8>>();
        [vec![4u8; width + 1], num_bytes_table]
            .concat()
            .into_iter()
            .take(width * height)
            .collect()
    }
}

/// Main struct for reading XIM images.
#[gen_stub_pyclass]
#[pyclass]
pub struct XIMImage {
    #[pyo3(get)]
    pub header: XIMHeader,
    pixel_data: PixelDataSupported,
    pub histogram: XIMHistogram,
    pub properties: XIMProperties,
}

#[derive(IntoPyObject)]
pub enum XIMArray<'py> {
    #[pyo3(transparent)]
    Int8(Bound<'py, PyArray2<i8>>),
    #[pyo3(transparent)]
    Int16(Bound<'py, PyArray2<i16>>),
    #[pyo3(transparent)]
    Int32(Bound<'py, PyArray2<i32>>),
    #[pyo3(transparent)]
    Int64(Bound<'py, PyArray2<i64>>),
}

impl_stub_type!(XIMArray<'_> = PyArray2<i8> | PyArray2<i16> | PyArray2<i32> | PyArray2<i64>);

/// Represents XIM Header
#[derive(Debug, Clone, BinRead)]
#[gen_stub_pyclass]
#[pyclass]
#[br(little)]
pub struct XIMHeader {
    #[pyo3(get)]
    #[br(little, try_map=|x: [u8; 8]| String::from_utf8(x.to_vec()))]
    pub identifier: String,
    #[pyo3(get)]
    pub version: i32,
    #[pyo3(get)]
    pub width: i32,
    #[pyo3(get)]
    pub height: i32,
    #[pyo3(get)]
    pub bits_per_pixel: i32,
    #[pyo3(get)]
    pub bytes_per_pixel: i32,
    #[br(little, try_map=|x: i32| match x {
        0=>Ok(false),
        1=>Ok(true),
        _=> Err(Error::InvalidCompressionIndicator)
    })]
    pub is_compressed: bool,
}

#[derive(Debug, Clone)]
pub enum PixelDataSupported {
    Int8(PixelData<i8>),
    Int16(PixelData<i16>),
    Int32(PixelData<i32>),
    Int64(PixelData<i64>),
}

#[derive(Debug, Clone)]
pub struct PixelData<I>(ndarray::Array2<I>);

#[binread]
#[derive(Debug, Clone)]
#[gen_stub_pyclass]
#[pyclass]
pub struct XIMHistogram {
    #[br(temp)]
    bins: i32,
    #[br(count=bins)]
    #[pyo3(get)]
    pub histogram: Vec<i32>,
}

#[binread]
#[br(little)]
#[gen_stub_pyclass]
#[pyclass]
#[derive(Debug, Clone)]
pub struct XIMProperties {
    #[br(temp)]
    num_properties: i32,
    #[br(count=num_properties, map=|val: Vec<Property>| HashMap::from_iter(val.into_iter().map(|x| (x.property_name, x.property_value) )))]
    pub properties: HashMap<String, PropertyValue>,
}

#[binread]
#[br(little)]
#[derive(Debug, Clone)]
pub struct Property {
    #[br(temp)]
    property_name_len: i32,
    #[br(little, count=property_name_len, try_map=|x: Vec<u8>| String::from_utf8(x))]
    pub property_name: String,
    pub property_value: PropertyValue,
}

#[binread]
#[br(little)]
#[derive(Debug, Clone, IntoPyObject)]
pub enum PropertyValue {
    #[br(magic = 0i32)]
    #[pyo3(transparent)]
    Integer(i32),
    #[br(magic = 1i32)]
    #[pyo3(transparent)]
    Double(f64),
    #[br(magic = 2i32)]
    #[pyo3(transparent)]
    String {
        #[br(temp)]
        len: i32,
        #[br(little, count=len, try_map=|x: Vec<u8>| String::from_utf8(x))]
        val: String,
    },
    #[br(magic = 4i32)]
    #[pyo3(transparent)]
    DoubleArray {
        #[br(temp)]
        len: i32,
        #[br(count=len/8)]
        val: Vec<f64>,
    },
    #[br(magic = 5i32)]
    #[pyo3(transparent)]
    IntegerArray {
        #[br(temp)]
        len: i32,
        #[br(count=len/4)]
        val: Vec<i32>,
    },
}

#[binread]
#[br(little, import{width: usize, height: usize})]
#[derive(Debug, Clone)]
struct CompressedPixelBuffer {
    #[br(temp)]
    lookup_table_len: i32,
    #[br(count=lookup_table_len, map=parse_lookup(width, height))]
    pub lookup_table: Vec<u8>,
    #[br(temp)]
    compressed_pixel_buffer_len: i32,
    #[br(count=compressed_pixel_buffer_len)]
    pub compressed_pixel_buffer: Vec<u8>,
    _uncompressed_pixel_buffer_len: i32,
}

impl_stub_type!(PropertyValue = i32 | f64 | String | Vec<f64> | Vec<i32>);

impl XIMImage {
    /// Constructor for XIMImage. Must implement Read and Seek.
    pub fn from_reader<R: Read + Seek>(mut reader: R) -> Result<Self> {
        let header = XIMHeader::from_reader(&mut reader)?;
        let pixel_data = if header.is_compressed {
            PixelDataSupported::from_compressed(&mut reader, &header)?
        } else {
            PixelDataSupported::from_uncompressed(&mut reader, &header)?
        };
        let histogram = XIMHistogram::from_reader(&mut reader)?;
        let properties = XIMProperties::from_reader(&mut reader)?;
        Ok(Self {
            header,
            pixel_data,
            histogram,
            properties,
        })
    }
}

#[gen_stub_pymethods]
#[pymethods]
impl XIMImage {
    /// Create XIMImage from path
    #[new]
    pub fn new(image_path: PathBuf) -> PyResult<Self> {
        let file = File::open(image_path)?;
        let reader = BufReader::new(file);
        Ok(Self::from_reader(reader)?)
    }

    /// Gets a numpy view of the image array.
    #[getter]
    pub fn numpy<'py>(this: Bound<'py, Self>) -> XIMArray<'py> {
        match &this.borrow().pixel_data {
            PixelDataSupported::Int8(pixel_data) => {
                let array = &pixel_data.0;
                unsafe {
                    let pyarray = PyArray2::borrow_from_array(array, this.into_any());
                    pyarray.readwrite().make_nonwriteable();
                    XIMArray::Int8(pyarray)
                }
            }
            PixelDataSupported::Int16(pixel_data) => {
                let array = &pixel_data.0;
                unsafe {
                    let pyarray = PyArray2::borrow_from_array(array, this.into_any());
                    pyarray.readwrite().make_nonwriteable();
                    XIMArray::Int16(pyarray)
                }
            }
            PixelDataSupported::Int32(pixel_data) => {
                let array = &pixel_data.0;
                unsafe {
                    let pyarray = PyArray2::borrow_from_array(array, this.into_any());
                    pyarray.readwrite().make_nonwriteable();
                    XIMArray::Int32(pyarray)
                }
            }
            PixelDataSupported::Int64(pixel_data) => {
                let array = &pixel_data.0;
                unsafe {
                    let pyarray = PyArray2::borrow_from_array(array, this.into_any());
                    pyarray.readwrite().make_nonwriteable();
                    XIMArray::Int64(pyarray)
                }
            }
        }
    }

    /// Gets a list of histogram values, with the bins increasing with index.
    #[getter]
    pub fn histogram(&self) -> Vec<i32> {
        self.histogram.histogram.clone()
    }

    /// Gets a dictionary of properties from the image.
    #[getter]
    pub fn properties(&self) -> HashMap<String, PropertyValue> {
        self.properties.properties.clone()
    }
}

impl XIMHeader {
    pub fn from_reader<R: Read + Seek>(reader: &mut R) -> Result<Self> {
        Ok(Self::read(reader)?)
    }

    pub fn width(&self) -> Result<usize> {
        usize::try_from(self.width).map_err(|_err| Error::InvalidWidth)
    }

    pub fn height(&self) -> Result<usize> {
        usize::try_from(self.height).map_err(|_err| Error::InvalidHeight)
    }
}

impl<I> PixelData<I> {
    pub fn new(array: ndarray::Array2<I>) -> Self {
        Self(array)
    }
}

impl PixelDataSupported {
    fn read_to_arr<I, R>(mut reader: R, width: usize, height: usize) -> Result<PixelData<I>>
    where
        I: num_traits::ConstZero + Clone + Copy,
        R: Read + ReadFromReader<I>,
    {
        let array = {
            let mut data: Vec<I> = vec![I::ZERO; width * height];
            let _ = ReadFromReader::<I>::read_type_into::<LE>(&mut reader, &mut data)
                .map_err(|_err| Error::InvalidPixels)?;
            ndarray::Array2::from_shape_vec((width, height), data)?
        };
        Ok(PixelData::new(array))
    }

    fn from_uncompressed(mut reader: impl Read, header: &XIMHeader) -> Result<Self> {
        let num_bytes = header.bytes_per_pixel;

        let width = header.width()?;
        let height = header.height()?;

        let _pixel_buffer_size = read_i32_as_usize(&mut reader, Error::InvalidPixelBufferSize)?;

        match num_bytes {
            1 => Self::read_to_arr(&mut reader, width, height).map(Self::Int8),
            2 => Self::read_to_arr(&mut reader, width, height).map(Self::Int16),
            4 => Self::read_to_arr(&mut reader, width, height).map(Self::Int32),
            8 => Self::read_to_arr(&mut reader, width, height).map(Self::Int64),
            _ => todo!(),
        }
    }

    fn decompress_array<I>(
        compressed_pixel_buffer: Vec<u8>,
        num_bytes_table: impl Iterator<Item = u8>,
        width: usize,
        height: usize,
    ) -> Result<PixelData<I>>
    where
        I: num_traits::ConstZero
            + TryFrom<i32>
            + TryFrom<i8>
            + TryFrom<i16>
            + Clone
            + Copy
            + num_traits::WrappingAdd
            + num_traits::WrappingSub,
    {
        let lookup_table = num_bytes_table;
        let mut compressed_diffs = compressed_pixel_buffer.as_slice();

        let differences = lookup_table
            .map(|num_bytes| match num_bytes {
                1 => compressed_diffs
                    .read_i8()
                    .map_err(|_err| Error::InvalidPixels)
                    .and_then(|x| I::try_from(x).map_err(|_err| Error::InvalidPixels)),
                2 => compressed_diffs
                    .read_i16::<LE>()
                    .map_err(|_err| Error::InvalidPixels)
                    .and_then(|x| I::try_from(x).map_err(|_err| Error::InvalidPixels)),
                4 => compressed_diffs
                    .read_i32::<LE>()
                    .map_err(|_err| Error::InvalidPixels)
                    .and_then(|x| I::try_from(x).map_err(|_err| Error::InvalidPixels)),
                _ => todo!(),
            })
            .collect::<Result<Vec<I>>>()?;

        let array = {
            let uncompressed_data = differences;
            let uncompressed_data = Self::decompress_diffs(uncompressed_data, width)?;
            let array = ndarray::Array2::from_shape_vec((height, width), uncompressed_data)?;
            array
        };

        Ok(PixelData::new(array))
    }

    fn from_compressed<R: Read + Seek>(mut reader: R, header: &XIMHeader) -> Result<Self> {
        let width = header.width()?;
        let height = header.height()?;

        let compressed_buffer =
            CompressedPixelBuffer::read_le_args(&mut reader, args! {width, height})?;

        let lookup_table = compressed_buffer.lookup_table.into_iter();

        let compressed_pixel_buffer = compressed_buffer.compressed_pixel_buffer;

        let pixel_data = match header.bytes_per_pixel {
            1 => {
                let arr =
                    Self::decompress_array(compressed_pixel_buffer, lookup_table, width, height)?;
                PixelDataSupported::Int8(arr)
            }
            2 => {
                let arr =
                    Self::decompress_array(compressed_pixel_buffer, lookup_table, width, height)?;
                PixelDataSupported::Int16(arr)
            }
            4 => {
                let arr =
                    Self::decompress_array(compressed_pixel_buffer, lookup_table, width, height)?;
                PixelDataSupported::Int32(arr)
            }
            _ => todo!(),
        };

        Ok(pixel_data)
    }

    fn decompress_diffs<I>(mut compressed_arr: Vec<I>, width: usize) -> Result<Vec<I>>
    where
        I: num_traits::WrappingAdd + num_traits::WrappingSub + Copy,
    {
        let arr = compressed_arr.as_mut_slice();
        let first_index = width + 1;
        for i in first_index..arr.len() {
            let [left, above, upper_left] = (|| {
                Some([
                    *arr.get(i - 1)?,
                    *arr.get(i - width)?,
                    *arr.get(i - width - 1)?,
                ])
            })()
            .ok_or(Error::FailedDecompression)?;

            let diff = arr.get_mut(i).ok_or(Error::FailedDecompression)?;
            *diff = diff
                .wrapping_add(&left)
                .wrapping_add(&above)
                .wrapping_sub(&upper_left);
        }
        Ok(compressed_arr)
    }
}

impl XIMHistogram {
    pub fn from_reader<R: Read + Seek>(mut reader: R) -> Result<Self> {
        Ok(Self::read_le(&mut reader)?)
    }
}

impl XIMProperties {
    pub fn from_reader<R: Read + Seek>(mut reader: R) -> Result<Self> {
        Ok(Self::read_le(&mut reader)?)
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_decompression() {
        let input: [i16; 8] = [4, 3, 10, 1, 10, 30, 20, 40];
        let input_array = input.to_vec();
        let calculated_output = PixelDataSupported::decompress_diffs(input_array, 2)
            .expect("Failed to decompress diffs");
        let output = vec![4, 3, 10, 10, 27, 57, 94, 164];
        assert_eq!(calculated_output, output);
    }

    #[test]
    fn test_parse_lookup() {
        let test: Vec<u8> = vec![1, 10, 30, 20, 40];
        println!("{:#010b}", test.get(1).unwrap());
        let test = test
            .into_iter()
            .map(|val| val.to_le_bytes().to_vec())
            .collect::<Vec<_>>()
            .concat();
        let output: Vec<u8> = vec![2, 1, 1, 1, 4, 4, 1, 1, 4, 8, 2, 1, 1, 2, 2, 1, 1, 4, 4, 1];
        let calculated_output = parse_lookup(1, output.len())(test);
        let output: Vec<u8> = vec![4, 4, 2, 1, 1, 1, 4, 4, 1, 1, 4, 8, 2, 1, 1, 2, 2, 1, 1, 4];
        assert_eq!(output, calculated_output);
    }
}
