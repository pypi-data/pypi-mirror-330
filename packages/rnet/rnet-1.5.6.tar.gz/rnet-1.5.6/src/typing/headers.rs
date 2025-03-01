use crate::error::{wrap_invali_header_name_error, wrap_invali_header_value_error};
use pyo3::{
    prelude::*,
    types::{PyBytes, PyDict, PyList},
};
use pyo3_stub_gen::{PyStubType, TypeInfo};
use rquest::header::{self, HeaderName, HeaderValue};
use std::{collections::HashSet, ops::Deref, str::FromStr};

/// A HTTP header map.
#[derive(Clone, Debug)]
pub struct HeaderMap(header::HeaderMap);

/// A list of header names in order.
#[derive(Clone, Debug)]
pub struct HeaderNameOrder(Vec<HeaderName>);

impl From<header::HeaderMap> for HeaderMap {
    fn from(map: header::HeaderMap) -> Self {
        HeaderMap(map)
    }
}

impl From<HeaderMap> for header::HeaderMap {
    fn from(map: HeaderMap) -> Self {
        map.0
    }
}

impl From<HeaderNameOrder> for Vec<HeaderName> {
    fn from(order: HeaderNameOrder) -> Self {
        order.0
    }
}

impl Deref for HeaderMap {
    type Target = header::HeaderMap;

    fn deref(&self) -> &Self::Target {
        &self.0
    }
}

impl PyStubType for HeaderMap {
    fn type_output() -> TypeInfo {
        TypeInfo {
            name: "typing.Dict[str, bytes]".to_owned(),
            import: HashSet::new(),
        }
    }
}

impl PyStubType for HeaderNameOrder {
    fn type_output() -> TypeInfo {
        TypeInfo {
            name: "typing.List[str]".to_owned(),
            import: HashSet::new(),
        }
    }
}

impl FromPyObject<'_> for HeaderMap {
    fn extract_bound(ob: &Bound<'_, PyAny>) -> PyResult<Self> {
        let dict = ob.downcast::<PyDict>()?;

        dict.iter()
            .try_fold(
                header::HeaderMap::with_capacity(dict.len()),
                |mut headers, (key, value)| {
                    let name = HeaderName::from_str(key.extract::<&str>()?)
                        .map_err(wrap_invali_header_name_error)?;
                    let value = HeaderValue::from_str(value.extract::<&str>()?)
                        .map_err(wrap_invali_header_value_error)?;
                    headers.insert(name, value);
                    Ok(headers)
                },
            )
            .map(HeaderMap)
    }
}

impl<'py> FromPyObject<'py> for HeaderNameOrder {
    fn extract_bound(ob: &Bound<'py, PyAny>) -> PyResult<Self> {
        let list = ob.downcast::<PyList>()?;
        list.iter()
            .try_fold(Vec::with_capacity(list.len()), |mut order, item| {
                let name = HeaderName::from_str(item.extract::<&str>()?)
                    .map_err(wrap_invali_header_name_error)?;
                order.push(name);
                Ok(order)
            })
            .map(HeaderNameOrder)
    }
}

impl<'py> IntoPyObject<'py> for HeaderMap {
    type Target = PyDict;

    type Output = Bound<'py, Self::Target>;

    type Error = PyErr;

    fn into_pyobject(self, py: Python<'py>) -> Result<Self::Output, Self::Error> {
        self.0
            .iter()
            .try_fold(PyDict::new(py), |dict, (name, value)| {
                dict.set_item(name.as_str(), PyBytes::new(py, value.as_bytes()))?;
                Ok(dict)
            })
    }
}

impl<'py> IntoPyObject<'py> for HeaderNameOrder {
    type Target = PyList;

    type Output = Bound<'py, Self::Target>;

    type Error = PyErr;

    fn into_pyobject(self, py: Python<'py>) -> Result<Self::Output, Self::Error> {
        PyList::new(py, self.0.iter().map(|name| name.as_str()))
    }
}
