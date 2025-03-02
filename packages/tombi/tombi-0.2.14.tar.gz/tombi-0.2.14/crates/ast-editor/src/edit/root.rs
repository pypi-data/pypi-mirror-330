use futures::FutureExt;
use schema_store::Accessor;

impl crate::Edit for ast::Root {
    fn edit<'a: 'b, 'b>(
        &'a self,
        accessors: &'a [schema_store::Accessor],
        schema_url: Option<&'a schema_store::SchemaUrl>,
        value_schema: Option<&'a schema_store::ValueSchema>,
        definitions: Option<&'a schema_store::SchemaDefinitions>,
        schema_context: &'a schema_store::SchemaContext<'a>,
    ) -> futures::future::BoxFuture<'b, Vec<crate::Change>> {
        async move {
            let mut changes = vec![];

            for item in self.items() {
                changes.extend(match item {
                    ast::RootItem::Table(table) => {
                        let mut accessors = vec![];
                        for key in table.header().unwrap().keys() {
                            let Ok(key_text) = key.try_to_raw_text(schema_context.toml_version)
                            else {
                                return changes;
                            };
                            accessors.push(Accessor::Key(key_text));
                        }
                        table
                            .edit(
                                &accessors,
                                schema_url,
                                value_schema,
                                definitions,
                                schema_context,
                            )
                            .await
                    }
                    ast::RootItem::ArrayOfTables(array_of_tables) => {
                        array_of_tables
                            .edit(
                                accessors,
                                schema_url,
                                value_schema,
                                definitions,
                                schema_context,
                            )
                            .await
                    }
                    ast::RootItem::KeyValue(key_value) => {
                        key_value
                            .edit(
                                accessors,
                                schema_url,
                                value_schema,
                                definitions,
                                schema_context,
                            )
                            .await
                    }
                });
            }

            changes
        }
        .boxed()
    }
}
