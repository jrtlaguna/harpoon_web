from django import forms
from django.urls import reverse

from vessels.models import Vessel

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Field, Div, HTML, Submit


CHARTER_TYPE_CHOICES = [("", "Select Charter Type")] + Vessel.CharterType.choices


class VesselForm(forms.Form):
    charter_type = forms.ChoiceField(
        choices=CHARTER_TYPE_CHOICES,
        label="Charter Type",
        widget=forms.widgets.Select(attrs={"placeholder": "Select Charter Type"}),
    )
    name = forms.CharField(
        max_length=80,
        label="Name of Vessel",
        widget=forms.TextInput(
            attrs={"placeholder": "Type Here"},
        ),
    )
    imo_number = forms.CharField(
        max_length=80,
        widget=forms.TextInput(
            attrs={"placeholder": "Type Here"},
        ),
    )

    def __init__(self, *args, **kwargs):
        imo_number = kwargs.pop("imo_number") or ""
        super().__init__(*args, **kwargs)

        self.helper = FormHelper(self)
        self.helper.form_id = "id-vesselForm"
        self.helper.label_class = "form-label"
        self.form_action = "vessels:vessel_setup"

        # FIELDS
        charter_type = Div(
            Field(
                "charter_type",
                css_class="form-select",
            ),
            css_class="col-12 col-md-6",
        )
        name = Div(
            Field("name", css_class="form-control"),
            css_class="col-12",
        )
        imo_number = Div(
            HTML(
                f"""
                <div class="form-group">
                    <span for="" class="txt-color-gray">IMO # (International Maritime Organization #)</span>
                    <br>
                    <small class="txt-color-gray font-italic">This vessel identification number can be located in the bridge on the ship’s certificates.</small>

                    <div class="d-flex mt-2 align-items-center">
                        <label for="" class="form-label mr-2">IMO- </label>
                        <input type="text" name="imo_number" class="form-control" value="{imo_number}" placeholder="Type Here">
                    </div>
                </div>
                """
            ),
            css_class="col-12",
        )

        submit_button = Submit(
            "submit",
            "Save and Continue",
            css_id="get_started",
        )
        submit_button.field_classes = "btn btn-solid-gold w-100"

        self.helper.layout = Layout(
            Div(
                Div(
                    HTML(
                        '<span class="fs-11 fw-700 txt-color-gray text-uppercase">VESSEL Details</span>'
                    ),
                    Div(
                        charter_type,
                        name,
                        imo_number,
                        css_class="form-row pl-3 pt-3 border-left-gray-80-1 mx-0",
                    ),
                    css_class="w-100 mb-4",
                ),
                Div(
                    submit_button,
                    css_class="col-md-5 px-md-0",
                ),
                css_class="col-12",
            )
        )


class VesselProfileForm(forms.Form):
    charter_type = forms.ChoiceField(
        choices=CHARTER_TYPE_CHOICES,
        label="Charter Type",
        widget=forms.widgets.Select(),
    )
    name = forms.CharField(
        max_length=80,
        label="Name of Vessel",
        widget=forms.TextInput(),
    )
    imo_number = forms.IntegerField(
        min_value=1,
        widget=forms.widgets.NumberInput(attrs={"placeholder": "Type Here"}),
    )

    def __init__(self, *args, **kwargs):
        instance_imo_number = kwargs.pop("imo_number")
        super().__init__(*args, **kwargs)

        self.helper = FormHelper(self)
        self.helper.form_id = "id-vesselForm"
        self.helper.label_class = "form-label"
        self.form_action = "vessels:profile_edit"

        # FIELDS
        charter_type = Div(
            Field(
                "charter_type",
                css_class="form-select",
            ),
            css_class="col-12",
        )
        name = Div(
            Field("name", css_class="form-control"),
            css_class="col-12",
        )
        imo_number = Div(
            HTML(
                f"""
                <div class="form-group">
                    <label for="" class="form-label">IMO # (International Maritime Organization #) </label>
                    <small class="form-short-description font-italic fs-12 mb-0 mt-0">This vessel identification number can be located in the bridge on the ship’s certificates.</small>
                    <div class="d-flex align-items-center">
                        <div class="mr-2">
                            <label for="" class="form-label">IMO - </label>
                        </div>
                        <div class="flex-fill">
                            <input type="text" name="imo_number" class="form-control" value="{instance_imo_number}" placeholder="Type Here">
                        </div>
                    </div>
                </div>
                """
            ),
            css_class="col-12",
        )

        self.helper.layout = Layout(
            Div(
                HTML(
                    """
                    <span class="fs-18 fw-700 txt-color-white text-uppercase">
                        Vessel Details
                    </span>
                """
                ),
                Div(
                    charter_type,
                    name,
                    imo_number,
                    css_class="form-row pl-3 pt-3 border-left-gray-80-1 mx-0",
                ),
                css_class="w-100 mb-4",
            )
        )


class VesselDocumentForm(forms.Form):
    document = forms.FileField(
        widget=forms.ClearableFileInput(attrs={"multiple": True}),
    )

    def __init__(self, *args, **kwargs):
        vessel_id = kwargs.pop("vessel_id")
        super().__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.form_id = "id-fileForm"
        self.helper.form_action = reverse("vessels:documents_upload", args=[vessel_id])
        # document_field = self.fields["document"]
        # document_field.widget = document_field.hidden_widget()
        upload_button = HTML(
            """
                <div class="col-12 align-items-center">
                    <div class="row">
                        <div class="col-md-6 w-100"><a href="javascript:void(0)" class="btn btn-solid-gold w-100" data-toggle="modal"
                                data-target="#documents_modal">View Documents</a></div>
                        <div class="col-md-6 w-100"><a id="documentButton" href="#" class="btn btn-outline-gold w-100">Upload Additional Documents</a>
                        </div>
                    </div>
                </div>
            """
        )
        document = Field("document", id="documentFile", hidden="hidden")

        self.helper.layout = Layout(upload_button, document)
