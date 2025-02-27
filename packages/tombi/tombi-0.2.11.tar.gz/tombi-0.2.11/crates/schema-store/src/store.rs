use ahash::AHashMap;
use config::SchemaCatalogItem;
use itertools::Either;
use std::{ops::Deref, sync::Arc};
use tokio::sync::RwLock;

use crate::{json::CatalogUrl, DocumentSchema, SchemaAccessor, SchemaUrl, SourceSchema};

#[derive(Debug, Clone, Default)]
pub struct SchemaStore {
    http_client: reqwest::Client,
    schemas: Arc<RwLock<AHashMap<SchemaUrl, Result<DocumentSchema, crate::Error>>>>,
    catalogs: Arc<RwLock<Vec<crate::CatalogSchema>>>,
}

impl SchemaStore {
    pub fn new() -> Self {
        Self {
            http_client: reqwest::Client::new(),
            schemas: Arc::new(RwLock::new(AHashMap::new())),
            catalogs: Arc::new(RwLock::new(Vec::new())),
        }
    }

    pub async fn load_schemas_from_config(
        &self,
        config_dirpath: Option<std::path::PathBuf>,
        schemas: &[SchemaCatalogItem],
    ) {
        let config_dirpath = match config_dirpath {
            Some(path) => path,
            None => std::env::current_dir().unwrap(),
        };
        let mut catalogs = self.catalogs.write().await;
        for schema in schemas.iter() {
            let Ok(url) = SchemaUrl::from_file_path(config_dirpath.join(schema.path())) else {
                continue;
            };
            tracing::debug!("load config schema from: {}", url);

            catalogs.push(crate::CatalogSchema {
                url,
                include: schema.include().to_vec(),
                toml_version: schema.toml_version(),
                root_keys: schema.root_keys().and_then(SchemaAccessor::parse),
            });
        }
    }

    pub async fn update_schema(&self, schema_url: &SchemaUrl) -> Result<bool, crate::Error> {
        if self.schemas.read().await.contains_key(schema_url) {
            let document_schema = self.try_fetch_document_schema_from_url(schema_url).await?;

            self.schemas
                .write()
                .await
                .insert(schema_url.clone(), Ok(document_schema));
            tracing::debug!("update schema: {}", schema_url);

            Ok(true)
        } else {
            Ok(false)
        }
    }

    pub async fn load_catalog_from_url(
        &self,
        catalog_url: &CatalogUrl,
    ) -> Result<(), crate::Error> {
        tracing::debug!("loading schema catalog: {}", catalog_url);

        if let Ok(response) = self.http_client.get(catalog_url.as_str()).send().await {
            match response.json::<crate::json::Catalog>().await {
                Ok(catalog) => {
                    let mut catalogs = self.catalogs.write().await;
                    for catalog_schema in catalog.schemas {
                        if catalog_schema
                            .file_match
                            .iter()
                            .any(|pattern| pattern.ends_with(".toml"))
                        {
                            catalogs.push(crate::CatalogSchema {
                                url: catalog_schema.url,
                                include: catalog_schema.file_match,
                                toml_version: None,
                                root_keys: None,
                            });
                        }
                    }
                    Ok(())
                }
                Err(err) => Err(crate::Error::InvalidJsonFormat {
                    url: catalog_url.deref().clone(),
                    reason: err.to_string(),
                }),
            }
        } else {
            Err(crate::Error::CatalogUrlFetchFailed {
                catalog_url: catalog_url.clone(),
            })
        }
    }

    pub async fn add_json_schema(&self, json_schema: crate::json::JsonSchema) {
        let mut catalogs = self.catalogs.write().await;
        if json_schema
            .file_match
            .iter()
            .any(|pattern| pattern.ends_with(".toml"))
        {
            catalogs.push(crate::CatalogSchema {
                url: json_schema.url,
                include: json_schema.file_match,
                toml_version: None,
                root_keys: None,
            });
        }
    }

    async fn try_fetch_document_schema_from_url(
        &self,
        schema_url: &SchemaUrl,
    ) -> Result<DocumentSchema, crate::Error> {
        let schema: serde_json::Map<String, serde_json::Value> = match schema_url.scheme() {
            "file" => {
                let schema_path =
                    schema_url
                        .to_file_path()
                        .map_err(|_| crate::Error::InvalidFilePath {
                            url: schema_url.deref().to_owned(),
                        })?;
                let file = std::fs::File::open(&schema_path)
                    .map_err(|_| crate::Error::SchemaFileReadFailed { schema_path })?;

                serde_json::from_reader(file)
            }
            "http" | "https" => {
                tracing::debug!("fetch schema from url: {}", schema_url);

                let response = self
                    .http_client
                    .get(schema_url.as_ref())
                    .send()
                    .await
                    .map_err(|err| crate::Error::SchemaFetchFailed {
                        schema_url: schema_url.clone(),
                        reason: err.to_string(),
                    })?;

                let bytes =
                    response
                        .bytes()
                        .await
                        .map_err(|err| crate::Error::SchemaFetchFailed {
                            schema_url: schema_url.clone(),
                            reason: err.to_string(),
                        })?;

                serde_json::from_reader(std::io::Cursor::new(bytes))
            }
            _ => {
                return Err(crate::Error::SchemaUrlUnsupported {
                    schema_url: schema_url.to_owned(),
                })
            }
        }
        .map_err(|err| crate::Error::SchemaFileParseFailed {
            schema_url: schema_url.to_owned(),
            reason: err.to_string(),
        })?;

        Ok(DocumentSchema::new(schema, schema_url.clone()))
    }

    pub async fn try_load_document_schema(
        &self,
        schema_url: &SchemaUrl,
    ) -> Result<DocumentSchema, crate::Error> {
        if let Some(document_schema) = self.schemas.read().await.get(schema_url) {
            return match document_schema {
                Ok(document_schema) => Ok(document_schema.clone()),
                Err(err) => Err(err.clone()),
            };
        }

        let document_schema = {
            let mut schemas = self.schemas.write().await;

            let document_schema = self.try_fetch_document_schema_from_url(schema_url).await?;

            schemas.insert(schema_url.to_owned(), Ok(document_schema.clone()));

            document_schema
        };

        Ok(document_schema)
    }

    pub async fn try_get_source_schema_from_url(
        &self,
        source_url: &url::Url,
    ) -> Result<Option<SourceSchema>, crate::Error> {
        match source_url.scheme() {
            "file" => {
                let source_path =
                    source_url
                        .to_file_path()
                        .map_err(|_| crate::Error::SourceUrlParseFailed {
                            source_url: source_url.to_owned(),
                        })?;
                self.try_get_source_schema_from_path(&source_path).await
            }
            "http" | "https" => {
                let schema_url = SchemaUrl::new(source_url.clone());
                let document_schema = self.try_load_document_schema(&schema_url).await?;

                Ok(Some(SourceSchema {
                    root_schema: Some(document_schema),
                    sub_schema_url_map: Default::default(),
                }))
            }
            "untitled" => Ok(None),
            _ => Err(crate::Error::SourceUrlUnsupported {
                source_url: source_url.to_owned(),
            }),
        }
    }

    pub async fn try_get_source_schema_from_path(
        &self,
        source_path: &std::path::Path,
    ) -> Result<Option<SourceSchema>, crate::Error> {
        let mut source_schema: Option<SourceSchema> = None;

        let catalogs = self.catalogs.read().await;
        let matching_schemas: Vec<_> = {
            catalogs
                .iter()
                .filter(|catalog| {
                    catalog.include.iter().any(|pat| {
                        let pattern = if !pat.contains("*") {
                            format!("**/{}", pat)
                        } else {
                            pat.to_string()
                        };
                        glob::Pattern::new(&pattern)
                            .ok()
                            .map(|glob_pat| glob_pat.matches_path(source_path))
                            .unwrap_or(false)
                    })
                })
                .collect()
        };

        for matching_schema in matching_schemas {
            if let Ok(document_schema) = self.try_load_document_schema(&matching_schema.url).await {
                match &matching_schema.root_keys {
                    Some(root_keys) => match source_schema {
                        Some(ref mut source_schema) => {
                            if !source_schema.sub_schema_url_map.contains_key(root_keys) {
                                source_schema
                                    .sub_schema_url_map
                                    .insert(root_keys.clone(), document_schema.schema_url);
                            }
                        }
                        None => {
                            let mut new_source_schema = SourceSchema {
                                root_schema: None,
                                sub_schema_url_map: Default::default(),
                            };
                            new_source_schema
                                .sub_schema_url_map
                                .insert(root_keys.clone(), document_schema.schema_url);

                            source_schema = Some(new_source_schema);
                        }
                    },
                    None => match source_schema {
                        Some(ref mut source_schema) => {
                            if source_schema.root_schema.is_none() {
                                source_schema.root_schema = Some(document_schema);
                            }
                        }
                        None => {
                            source_schema = Some(SourceSchema {
                                root_schema: Some(document_schema),
                                sub_schema_url_map: Default::default(),
                            });
                        }
                    },
                }
            }
        }

        Ok(source_schema)
    }

    pub async fn try_get_source_schema(
        &self,
        source_url_or_path: Either<&url::Url, &std::path::Path>,
    ) -> Result<Option<SourceSchema>, crate::Error> {
        match source_url_or_path {
            Either::Left(source_url) => self
                .try_get_source_schema_from_url(source_url)
                .await
                .inspect(|_| {
                    tracing::debug!("find schema from url: {}", source_url);
                }),
            Either::Right(source_path) => self
                .try_get_source_schema_from_path(source_path)
                .await
                .inspect(|_| {
                    tracing::debug!("find schema from source: {}", source_path.display());
                }),
        }
    }
}
