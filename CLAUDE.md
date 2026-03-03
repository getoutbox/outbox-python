# SDK conventions

- Never expose resource names. Always use the IDs.
  - For example, a field with `author` with the resource name format of `parents/[parent_id]/resources/[id]` should be author_parent_id and author_id.
- Use namespaces.
  - For example, instead of create_message, do messages.create.
- Create your own SDK types based on the protobuf types.
