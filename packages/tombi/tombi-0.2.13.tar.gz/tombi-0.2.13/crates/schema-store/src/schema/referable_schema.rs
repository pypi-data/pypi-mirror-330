use std::borrow::Cow;

use futures::future::BoxFuture;

use super::{AllOfSchema, AnyOfSchema, OneOfSchema, SchemaDefinitions, SchemaUrl, ValueSchema};

#[derive(Debug, Clone, PartialEq)]
pub enum Referable<T> {
    Resolved {
        schema_url: Option<SchemaUrl>,
        value: T,
    },
    Ref {
        reference: String,
        title: Option<String>,
        description: Option<String>,
    },
}

pub struct CurrentSchema<'a> {
    pub schema_url: Cow<'a, SchemaUrl>,
    pub value_schema: &'a ValueSchema,
    pub definitions: &'a SchemaDefinitions,
}

impl<T> Referable<T> {
    pub fn resolved(&self) -> Option<&T> {
        match self {
            Self::Resolved { value, .. } => Some(value),
            Self::Ref { .. } => None,
        }
    }
}

impl Referable<ValueSchema> {
    pub fn new(object: &serde_json::Map<String, serde_json::Value>) -> Option<Self> {
        if let Some(serde_json::Value::String(ref_string)) = object.get("$ref") {
            return Some(Referable::Ref {
                reference: ref_string.clone(),
                title: object
                    .get("title")
                    .and_then(|title| title.as_str().map(|s| s.to_string())),
                description: object
                    .get("description")
                    .and_then(|description| description.as_str().map(|s| s.to_string())),
            });
        }

        ValueSchema::new(object).map(|value_schema| Referable::Resolved {
            schema_url: None,
            value: value_schema,
        })
    }

    pub async fn value_type(&self) -> crate::ValueType {
        match self {
            Referable::Resolved { value, .. } => value.value_type().await,
            Referable::Ref { .. } => unreachable!("unreachable ref value_tyle."),
        }
    }

    pub fn resolve<'a: 'b, 'b>(
        &'a mut self,
        schema_url: Cow<'a, SchemaUrl>,
        definitions: &'a SchemaDefinitions,
        schema_store: &'a crate::SchemaStore,
    ) -> BoxFuture<'b, Result<CurrentSchema<'a>, crate::Error>> {
        Box::pin(async move {
            match self {
                Referable::Ref {
                    reference,
                    title,
                    description,
                } => {
                    if let Some(definition_schema) = definitions.read().await.get(reference) {
                        let mut referable_schema = definition_schema.to_owned();
                        if let Referable::Resolved { ref mut value, .. } = &mut referable_schema {
                            if title.is_some() || description.is_some() {
                                value.set_title(title.to_owned());
                                value.set_description(description.to_owned());
                            }
                        }

                        *self = referable_schema;
                    } else if is_online_url(reference) {
                        let schema_url = SchemaUrl::parse(reference)?;
                        let document_schema =
                            schema_store.try_load_document_schema(&schema_url).await?;

                        if let Some(value_schema) = document_schema.value_schema {
                            *self = Referable::Resolved {
                                schema_url: Some(schema_url.clone()),
                                value: value_schema,
                            };
                            return self
                                .resolve(Cow::Owned(schema_url), definitions, schema_store)
                                .await;
                        } else {
                            return Err(crate::Error::InvalidJsonSchemaReference {
                                reference: reference.to_owned(),
                            });
                        }
                    } else {
                        return Err(crate::Error::UnsupportedReference {
                            reference: reference.to_owned(),
                        });
                    }

                    self.resolve(schema_url, definitions, schema_store).await
                }
                Referable::Resolved {
                    schema_url: reference_url,
                    value,
                    ..
                } => {
                    let schema_url = match reference_url {
                        Some(reference_url) => Cow::Borrowed(reference_url),
                        None => schema_url,
                    };
                    match value {
                        ValueSchema::OneOf(OneOfSchema { schemas, .. })
                        | ValueSchema::AnyOf(AnyOfSchema { schemas, .. })
                        | ValueSchema::AllOf(AllOfSchema { schemas, .. }) => {
                            for schema in schemas.write().await.iter_mut() {
                                schema
                                    .resolve(schema_url.clone(), definitions, schema_store)
                                    .await?;
                            }
                        }
                        _ => {}
                    }

                    Ok(CurrentSchema {
                        schema_url,
                        value_schema: value,
                        definitions,
                    })
                }
            }
        })
    }
}

pub fn is_online_url(reference: &str) -> bool {
    reference.starts_with("https://") || reference.starts_with("http://")
}
