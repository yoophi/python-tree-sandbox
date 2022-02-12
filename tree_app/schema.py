from tree_app.extensions import ma


class NodeSchema(ma.Schema):
    class Meta:
        fields = ("id", "name", 'children', '_links')

    children = ma.Nested('NodeSchema', many=True)

    # Smart hyperlinking
    _links = ma.Hyperlinks(
        {
            "self": ma.URLFor("node_detail", values=dict(id="<id>", _external=True), ),
            # "collection": ma.URLFor("nodes"),
        }
    )
