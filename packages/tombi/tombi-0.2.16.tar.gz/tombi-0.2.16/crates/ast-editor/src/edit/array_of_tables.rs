use ast::AstNode;
use futures::FutureExt;
use schema_store::{AnyOfSchema, CurrentSchema, OneOfSchema, ValueSchema};
use std::borrow::Cow;

impl crate::Edit for ast::ArrayOfTables {
    fn edit<'a: 'b, 'b>(
        &'a self,
        accessors: &'a [schema_store::Accessor],
        schema_url: Option<&'a schema_store::SchemaUrl>,
        value_schema: Option<&'a schema_store::ValueSchema>,
        definitions: Option<&'a schema_store::SchemaDefinitions>,
        schema_context: &'a schema_store::SchemaContext<'a>,
    ) -> futures::future::BoxFuture<'b, Vec<crate::Change>> {
        tracing::trace!("accessors: {:?}", accessors);
        tracing::trace!("schema_url: {:?}", schema_url);
        tracing::trace!("value_schema: {:?}", value_schema);

        async move {
            let mut changes = vec![];
            for key_value in self.key_values() {
                changes.extend(
                    key_value
                        .edit(
                            &accessors,
                            schema_url,
                            value_schema,
                            definitions,
                            schema_context,
                        )
                        .await,
                );
            }

            match (schema_url, value_schema, definitions) {
                (Some(schema_url), Some(value_schema), Some(definitions)) => match value_schema {
                    ValueSchema::Table(table_schema) => {
                        if accessors.is_empty() {
                            changes.extend(
                                crate::rule::table_keys_order_by(self.syntax(), table_schema).await,
                            );
                            return changes;
                        }
                        let mut properties = table_schema.properties.write().await;
                        if let Some(referable_property_schema) = properties.get_mut(&accessors[0]) {
                            if let Ok(Some(CurrentSchema {
                                value_schema,
                                schema_url,
                                definitions,
                            })) = referable_property_schema
                                .resolve(
                                    Cow::Borrowed(schema_url),
                                    Cow::Borrowed(definitions),
                                    schema_context.store,
                                )
                                .await
                            {
                                return self
                                    .edit(
                                        &accessors[1..],
                                        Some(&schema_url),
                                        Some(value_schema),
                                        Some(&definitions),
                                        schema_context,
                                    )
                                    .await;
                            };
                        } else if let Some(pattern_properties) = &table_schema.pattern_properties {
                            for (property_key, referable_property_schema) in
                                pattern_properties.write().await.iter_mut()
                            {
                                if let Ok(pattern) = regex::Regex::new(property_key) {
                                    if pattern.is_match(&accessors[0].to_string()) {
                                        if let Ok(Some(CurrentSchema {
                                            value_schema,
                                            schema_url,
                                            definitions,
                                        })) = referable_property_schema
                                            .resolve(
                                                Cow::Borrowed(schema_url),
                                                Cow::Borrowed(definitions),
                                                schema_context.store,
                                            )
                                            .await
                                        {
                                            return self
                                                .edit(
                                                    &accessors[1..],
                                                    Some(&schema_url),
                                                    Some(value_schema),
                                                    Some(&definitions),
                                                    schema_context,
                                                )
                                                .await;
                                        }
                                    }
                                }
                            }
                        } else if let Some(referable_additional_property_schema) =
                            &table_schema.additional_property_schema
                        {
                            let mut referable_schema =
                                referable_additional_property_schema.write().await;
                            if let Ok(Some(CurrentSchema {
                                schema_url,
                                value_schema,
                                definitions,
                            })) = referable_schema
                                .resolve(
                                    Cow::Borrowed(schema_url),
                                    Cow::Borrowed(definitions),
                                    schema_context.store,
                                )
                                .await
                            {
                                return self
                                    .edit(
                                        &accessors[1..],
                                        Some(&schema_url),
                                        Some(value_schema),
                                        Some(&definitions),
                                        schema_context,
                                    )
                                    .await;
                            }
                        }
                    }
                    ValueSchema::OneOf(OneOfSchema { schemas, .. })
                    | ValueSchema::AnyOf(AnyOfSchema { schemas, .. }) => {
                        for schema in schemas.write().await.iter_mut() {
                            if let Ok(Some(CurrentSchema {
                                schema_url,
                                value_schema,
                                definitions,
                            })) = schema
                                .resolve(
                                    Cow::Borrowed(schema_url),
                                    Cow::Borrowed(definitions),
                                    schema_context.store,
                                )
                                .await
                            {
                                changes.extend(
                                    self.edit(
                                        &accessors,
                                        Some(&schema_url),
                                        Some(value_schema),
                                        Some(&definitions),
                                        schema_context,
                                    )
                                    .await,
                                );

                                if !changes.is_empty() {
                                    return changes;
                                }
                            }
                        }
                    }
                    _ => {}
                },
                _ => {}
            }

            changes
        }
        .boxed()
    }
}
