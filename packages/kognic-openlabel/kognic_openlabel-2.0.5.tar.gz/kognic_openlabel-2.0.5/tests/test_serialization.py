import kognic.openlabel.models as OLM

openlabel = OLM.OpenLabelAnnotation(
    openlabel=OLM.Openlabel(
        metadata=OLM.Metadata(schema_version=OLM.SchemaVersion.field_1_0_0),
        objects={
            "1": OLM.Object(name="the-name-1", type="the-type"),
            "2": OLM.Object(name="the-name-2", type="the-type"),
        },
        frames={
            "0": OLM.Frame(
                objects={
                    "1": OLM.Objects(
                        object_data=OLM.ObjectData(
                            text=[OLM.Text(name="the-text", val="hello")],
                            cuboid=[
                                OLM.Cuboid(
                                    name="a-cuboid", val=[1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
                                )
                            ],
                        )
                    ),
                    "2": OLM.Objects(
                        object_data=OLM.ObjectData(
                            num=[OLM.Num(name="the-num", val=1337)],
                            bbox=[OLM.Bbox(name="a-box", val=[10, 20, 30, 40])],
                        )
                    ),
                },
            ),
            "1": OLM.Frame(
                frame_properties=OLM.FrameProperties(timestamp=1),
                objects={
                    "1": OLM.Objects(
                        object_data=OLM.ObjectData(
                            text=[OLM.Text(name="the-text", val="hi")],
                            cuboid=[
                                OLM.Cuboid(
                                    name="a-cuboid", val=[1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
                                )
                            ],
                        ),
                    ),
                    "2": OLM.Objects(
                        object_data=OLM.ObjectData(
                            num=[OLM.Num(name="the-num", val=23.53232)],
                            bbox=[OLM.Bbox(name="a-box", val=[10, 20, 30, 40])],
                        )
                    ),
                },
            ),
        },
    ),
)

openlabel_tags = OLM.OpenLabelAnnotation(
    openlabel=OLM.Openlabel(
        metadata=OLM.Metadata(schema_version=OLM.SchemaVersion.field_1_0_0),
        tags={
            "1": OLM.Tag(
                ontology_uid="1",
                type="the-type",
                tag_data="it-should-parse-me-to-tag-data",
            ),
            "2": OLM.Tag(
                ontology_uid="2",
                type="the-type",
                tag_data=OLM.TagDatum(
                    text=[OLM.Text(name="the-text", val="hello")],
                ),
            ),
        },
    )
)


def test_serialization_round_trip():
    ol_dict = openlabel.model_dump(exclude_none=True)
    result = OLM.OpenLabelAnnotation(**ol_dict)
    assert result == openlabel


def test_serialization_round_trip_root_model():
    ol_dict = openlabel_tags.model_dump(exclude_none=True)
    result = OLM.OpenLabelAnnotation(**ol_dict)
    assert result == openlabel_tags
