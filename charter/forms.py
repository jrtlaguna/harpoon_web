import dis

from crispy_forms.bootstrap import FormActions
from crispy_forms.helper import FormHelper
from crispy_forms.layout import HTML, Div, Field, Layout, Submit
from django import forms
from django.templatetags.static import static

from authentication.models import User


class CharterDetailsForm(forms.Form):
    first_name = forms.CharField(label="First Name")
    last_name = forms.CharField(label="Last Name")
    email = forms.EmailField(label="Email Address")
    embark_city = forms.CharField(
        label="Embark Location",
    )
    embark_country = forms.CharField(
        label=" ",
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.helper = FormHelper(self)
        self.helper.form_id = "id-charterDetailsForm"
        self.helper.form_class = "form-container-profile ml-0"
        self.helper.form_method = "post"
        self.helper.label_class = "form-label"

        generate_booking_id = Submit(
            "submit",
            "Generate Booking ID",
        )
        generate_booking_id.field_classes = "btn btn-solid-gold w-100"

        separator = HTML(
            f"""
            <div class="separator">
                <div class="line"><hr></div>
                <div><img src="{static('core/img/form-sep-img.svg')}"></div>
                <div class="line"><hr></div>
            </div>
            """
        )

        apa_budget_field = Div(
            Div(
                Div(
                    HTML(
                        """
                    <span class="txt-color-dark-80 position-absolute fs-16 fw-700 input-group-addon currency-symbol" style="bottom:30px">$</span>
                            <label for="" class="form-label">Amount</label>
                            <input type="text" class="form-control currency-amount" id="inlineFormInputGroup" name="apa_budget" placeholder="0.00" size="8" value="{{apa_budget}}" required>
                    """
                    ),
                    css_class="form-group",
                ),
                css_class="col-6 col-sm-9",
            ),
            Div(
                Div(
                    HTML(
                        """
                    <label for="" class="form-label"></label>
                    <select class="currency-selector form-select" name="currency">
                        <option data-symbol="$" data-placeholder="0.00" value="USD" {% if currency == 'USD' %}selected{% endif %}>$ USD
                        </option>
                        <option data-symbol="€" data-placeholder="0.00" value="EURO" {% if currency == 'EURO' %}selected{% endif %}>€ Euro</option>
                        <option data-symbol="£" data-placeholder="0.00" value="POUNDS" {% if currency == 'POUNDS' %}selected{% endif %}>£ British Pounds</option>
                    </select>
                    """
                    ),
                    css_class="form-group",
                ),
                css_class="col",
            ),
            css_class="form-row pl-3 pt-3 border-left-gray-80-1 mx-0",
        )

        embark_date_field = Div(
            HTML(
                """
                <label for="" class="form-label">Date From</label>
                <div class="input-group align-items-center border-bottom-secondary-1">
                    <input type="text" autocomplete="off" class="form-control datepicker border-0" value="{{ embark_date }}" name="embark_date" placeholder="DD MM YYYY">
                    <div class="input-group-append">
                        <i class="far fa-calendar txt-color-white"></i>
                    </div>
                </div>
                """
            ),
            css_class="col-12 col-md-6",
        )

        disembark_date_field = Div(
            HTML(
                """
                <label for="" class="form-label">Date To</label>
                <div class="input-group align-items-center border-bottom-secondary-1">
                    <input type="text" autocomplete="off" class="form-control datepicker border-0" value="{{ disembark_date }}" name="disembark_date" placeholder="DD MM YYYY">
                    <div class="input-group-append">
                        <i class="far fa-calendar txt-color-white"></i>
                    </div>
                </div>
                """
            ),
            css_class="col-12 col-md-6",
        )

        self.helper.layout = Layout(
            Div(
                Div(
                    Div(
                        HTML(
                            """
                    <span class="fs-18 fw-700 txt-color-white text-uppercase">
                        Principal Info
                    </span>
                    """
                        ),
                        Div(
                            Div(
                                Field(
                                    "first_name",
                                    placeholder="First Name",
                                ),
                                css_class="col-12 col-md-6",
                            ),
                            Div(
                                Field(
                                    "last_name",
                                    placeholder="Last Name",
                                ),
                                css_class="col-12 col-md-6",
                            ),
                            Div(
                                Field(
                                    "email",
                                    placeholder="Email Address",
                                ),
                                css_class="col-12 col-md-12",
                            ),
                            css_class="form-row pl-3 pt-3 border-left-gray-80-1 mx-0",
                        ),
                        css_class="w-100",
                    ),
                    css_class="col-12",
                ),
                css_class="row",
            ),
            separator,
            Div(
                Div(
                    Div(
                        HTML(
                            """
                    <span class="fs-18 fw-700 txt-color-white text-uppercase">
                        SET APA BUDGET
                    </span>
                    """
                        ),
                        apa_budget_field,
                        css_class="w-100",
                    ),
                    css_class="col-12",
                ),
                css_class="row",
            ),
            separator,
            Div(
                Div(
                    Div(
                        HTML(
                            """
                    <span class="fs-18 fw-700 txt-color-white text-uppercase">
                        YACHT TRIP EMBARK
                    </span>
                    """
                        ),
                        Div(
                            Div(
                                Field(
                                    "embark_city",
                                    placeholder="City",
                                ),
                                css_class="col-12 col-md-6",
                            ),
                            Div(
                                Field(
                                    "embark_country",
                                    placeholder="Country",
                                ),
                                css_class="col-12 col-md-6",
                            ),
                            embark_date_field,
                            disembark_date_field,
                            css_class="form-row pl-3 pt-3 border-left-gray-80-1 mx-0",
                        ),
                        css_class="w-100 mb-4",
                    ),
                    css_class="col-md-12",
                ),
                css_class="row",
            ),
            Div(
                Div(FormActions(generate_booking_id), css_class="col-12 col-md-6"),
                css_class="row my-5",
            ),
        )

    def clean_email(self):
        email = self.cleaned_data.get("email")
        user = User.objects.filter(email=email)
        if user.exists() and user.last().is_admin:
            raise forms.ValidationError("Email should not be an admin.")

        return email


class CharterLocationsForm(forms.Form):
    embark_time = forms.CharField(
        label="Time", widget=forms.TextInput(attrs={"type": "time"})
    )
    disembark_time = forms.CharField(
        label="Time", widget=forms.TextInput(attrs={"type": "time"}), required=False
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.helper = FormHelper(self)
        self.helper.form_id = "id-charterLocationsForm"
        self.helper.form_class = (
            "w-100 bg-color-dark rounded-8 p-3 p-md-4 border-gold-1"
        )
        self.helper.form_method = "post"
        self.helper.label_class = "form-label"

        save_and_continue = Submit(
            "submit",
            "Save & Continue",
        )
        save_and_continue.field_classes = "btn btn-solid-gold w-100"

        embark_date_field = Div(
            HTML(
                """
                <div class="form-group">
                    <label for="" class="form-label">Date</label>
                    <div class="input-group align-items-center border-bottom-secondary-1">
                        <input type="text" class="form-control datepicker border-0" value="{{ embark_date }}" name="embark_date" placeholder="DD MM YYYY">
                        <div class="input-group-append">
                            <i class="far fa-calendar txt-color-white"></i>
                        </div>
                    </div>
                </div>
                """
            ),
            css_class="col-12 col-md-4",
        )

        embark_time_field = Div(
            HTML(
                """
                <label for="" class="form-label">Yacht Embark Time</label>
                <div class="input-group align-items-center border-bottom-secondary-1">
                    <input type="text" autocomplete="off" class="form-control timepicker border-0" name="embark_time" value="{{ embark_time }}" placeholder="HH:MM">
                    <div class="input-group-append">
                        <i class="far fa-clock txt-color-white"></i>
                    </div>
                </div>
                """
            ),
            css_class="col-12 col-md-4",
        )

        disembark_date_field = Div(
            HTML(
                """
                <div class="form-group">
                    <label for="" class="form-label">Date</label>
                    <div class="input-group align-items-center border-bottom-secondary-1">
                        <input type="text" class="form-control datepicker border-0" value="{{ disembark_date }}" name="disembark_date" placeholder="DD MM YYYY">
                        <div class="input-group-append">
                            <i class="far fa-calendar txt-color-white"></i>
                        </div>
                    </div>
                </div>
                """
            ),
            css_class="col-12 col-md-4",
        )

        disembark_time_field = Div(
            HTML(
                """
                <label for="" class="form-label">Yacht Disembark Time</label>
                <div class="input-group align-items-center border-bottom-secondary-1">
                    <input type="text" autocomplete="off" class="form-control timepicker border-0" name="disembark_time" value="{{ disembark_time }}" placeholder="HH:MM">
                    <div class="input-group-append">
                        <i class="far fa-clock txt-color-white"></i>
                    </div>
                </div>
                """
            ),
            css_class="col-12 col-md-4",
        )

        self.helper.layout = Layout(
            Div(
                Div(
                    Div(
                        HTML(
                            """
                        <span class="fs-11 fw-700 txt-color-gray text-uppercase">
                            Yacht  Trip Embark
                        </span>
                    """
                        ),
                        Div(
                            Div(
                                HTML(
                                    """
                                <label for="" class="form-label">Embark Location</label>
                                <input type="text" class="form-control textInput" value="{{ charter.embark_name_of_dock|default_if_none:"" }}" id="id_embark_name_of_dock" name="embark_name_of_dock" placeholder="Name of Dock / Yacht Club / Marina" required>
                                """
                                ),
                                css_class="col-12 col-md-12",
                            ),
                            Div(
                                HTML(
                                    '<input type="text" class="form-control textInput" value="{{ charter.embark_city|default_if_none:"" }}" id="id_embark_city" name="embark_city" placeholder="City" required>'
                                ),
                                css_class="col-12 col-md-6",
                            ),
                            Div(
                                HTML(
                                    '<input type="text" class="form-control textInput" value="{{ charter.embark_country|default_if_none:"" }}" id="id_embark_country" name="embark_country" placeholder="Country" required>'
                                ),
                                css_class="col-12 col-md-6",
                            ),
                            Div(
                                HTML(
                                    '<textarea class="form-control mt-2" rows="2" cols="20" id="id_embark_additional_info" name="embark_additional_info" placeholder="Additional Info">{{ charter.embark_additional_info|default_if_none:"" }}</textarea>'
                                ),
                                css_class="col-12 col-md-12",
                            ),
                            embark_date_field,
                            Div(css_class="col-12 col-md-8"),
                            embark_time_field,
                            Div(css_class="col-12 col-md-8"),
                            css_class="form-row pl-3 pt-3 border-left-gray-80-1 mx-0",
                        ),
                        css_class="w-100 mb-4",
                    ),
                    Div(
                        HTML(
                            """
                        <span class="fs-11 fw-700 txt-color-gray text-uppercase">
                            Yacht  Trip Disembark
                        </span>
                        """
                        ),
                        Div(
                            Div(
                                HTML(
                                    """
                                <label for="" class="form-label">Disembark Location</label>
                                <input type="text" class="form-control textInput" value="{{ charter.disembark_name_of_dock|default_if_none:"" }}" id="id_disembark_name_of_dock" name="disembark_name_of_dock" placeholder="Name of Dock / Yacht Club / Marina">
                                """
                                ),
                                css_class="col-12 col-md-12",
                            ),
                            Div(
                                HTML(
                                    '<input type="text" class="form-control textInput" value="{{ charter.disembark_city|default_if_none:"" }}" id="id_disembark_city" name="disembark_city" placeholder="City">'
                                ),
                                css_class="col-12 col-md-6",
                            ),
                            Div(
                                HTML(
                                    '<input type="text" class="form-control textInput" value="{{ charter.disembark_country|default_if_none:"" }}" id="id_disembark_country" name="disembark_country" placeholder="Country">'
                                ),
                                css_class="col-12 col-md-6",
                            ),
                            Div(
                                HTML(
                                    '<textarea class="form-control mt-2" rows="2" cols="20" id="id_disembark_additional_info" name="disembark_additional_info" placeholder="Additional Info">{{ charter.disembark_additional_info|default_if_none:"" }}</textarea>'
                                ),
                                css_class="col-12 col-md-12",
                            ),
                            disembark_date_field,
                            Div(css_class="col-12 col-md-8"),
                            disembark_time_field,
                            Div(css_class="col-12 col-md-8"),
                            css_class="form-row pl-3 pt-3 border-left-gray-80-1 mx-0",
                        ),
                        css_class="w-100 mb-4",
                    ),
                    Div(
                        Div(FormActions(save_and_continue), css_class="col-md-5 mb-3"),
                        css_class="form-row px-0 mx-0",
                    ),
                    css_class="col-12",
                ),
                css_class="form-container-profile ml-0",
            )
        )


class AddGuestsForm(forms.Form):
    def __init__(self, *args, **kwargs):
        added_guest_count = kwargs.pop("added_guest_count")
        charter = kwargs.pop("charter")
        super().__init__(*args, **kwargs)

        self.helper = FormHelper(self)
        self.helper.form_id = "id-charterLocationsForm"
        self.helper.form_class = "row"
        self.helper.form_method = "post"
        self.helper.label_class = "form-label"

        save_and_continue = Submit(
            "submit",
            "Save & Continue",
        )
        save_and_continue.field_classes = "btn btn-solid-gold w-100"

        field_name = "guest_email"
        if added_guest_count > 0:
            for i in range(added_guest_count):
                self.fields[field_name] = forms.CharField(required=False)
        else:
            self.fields[field_name] = forms.CharField(required=False)

        email_fields = []
        guests = charter.guests.all()
        if added_guest_count > 0:
            for i in range(added_guest_count):
                email_fields.append(
                    HTML(
                        f'<input type="text" class="form-control" value="{guests[i].email if len(guests) > i else ""}" id="id_guest_email_{str(i)}" name="guest_email" placeholder="Guest Email #{str(i + 1)}">'
                    )
                )
        else:
            email_fields.append(
                HTML(
                    """
                    <input type="text" class="form-control" value="" id="id_guest_email_0" name="guest_email" placeholder="Guest Email #1">
                    """
                )
            )

        self.helper.layout = Layout(
            Div(
                Div(
                    HTML(
                        """
                        <span class="fs-18 fw-700 txt-color-white text-uppercase">
                        Additional Guests
                        </span>
                    """
                    ),
                    Div(
                        Div(
                            HTML(
                                """
                                <small class="form-short-description">
                                    Please enter in emails of the guests below.
                                </small>
                            """
                            ),
                            css_class="col-12",
                        ),
                        Div(
                            Div(
                                *email_fields,
                                HTML(
                                    """
                                    <div id="new_guest"><input type="hidden" id="field_count" value="{% if charter.guests.all.count == 0 %}1{% else %}{{charter.guests.all.count}}{% endif %}"></div>
                                    <input type='button' class="btn btn-outline-gold fs-12 mt-5 add_guest" value='+ Add Guest'>
                                """
                                ),
                                css_class="form-group",
                            ),
                            css_class="col-12 col-md-8",
                        ),
                        Div(
                            HTML(
                                """
                                <small class="form-short-description fs-14">Upon completion of trip set up, the guests will receive an invite to Harpoon Solution to manage their trip.</small>
                                """
                            ),
                            css_class="col-12",
                        ),
                        css_class="form-row pl-3 pt-3 border-left-gray-80-1 mx-0",
                    ),
                    Div(
                        Div(FormActions(save_and_continue), css_class="col-md-5 mb-3"),
                        css_class="form-row px-0 mx-0",
                    ),
                    css_class="w-100 mb-4",
                ),
                css_class="col-12",
            )
        )


class AddGuestForm(forms.Form):
    email = forms.EmailField(label=" ")

    def __init__(self, *args, **kwargs):
        self.charter = kwargs.pop("charter")
        super().__init__(*args, **kwargs)

        self.helper = FormHelper(self)
        self.helper.form_id = "id-addGuestForm"
        self.helper.form_class = "form-row pl-3 pt-3 border-left-gray-80-1 mx-0"
        self.helper.form_method = "post"
        self.helper.label_class = "form-label"

        add_guest = Submit(
            "submit",
            "+ Add Guest",
        )
        add_guest.field_classes = "btn btn-outline-gold w-100"

        add_guest_form = Div(
            Div(
                Field("email", placeholder="Guest Email"), css_class="col-12 col-md-12"
            ),
            Div(
                Div(
                    Div(FormActions(add_guest), css_class="col-md-3 mb-3"),
                    css_class="form-row px-0 mx-0",
                ),
                css_class="col-12 col-md-12",
            ),
            css_class="col",
        )

        show_form = add_guest_form

        self.helper.layout = Layout(
            show_form,
        )


PREFERENCES_SHOPPING_CHOICES = [
    ("HEALTH_INFO", "Health Info"),
    ("FOOD", "Food"),
    ("BEVERAGES", "Beverages"),
    ("ALCOHOLIC", "Alcohol"),
    ("ROOM_AND_SERVICES", "Room & Services"),
    ("SIZING", "Sizing"),
]


class PreferencesShoppingListForm(forms.Form):
    def __init__(self, *args, **kwargs):
        self.charter = kwargs.pop("charter")

        super().__init__(*args, **kwargs)

        self.helper = FormHelper(self)
        self.helper.form_id = "id-PreferencesShoppingListForm"
        self.helper.form_class = "col-12"
        self.helper.form_method = "post"
        self.helper.label_class = "form-label"

        extract_button = Submit(
            "submit",
            "Download Shopping List",
        )
        extract_button.field_classes = "btn btn-solid-gold w-100"

        preferences_shopping_list_field = []
        for index, list_item in enumerate(PREFERENCES_SHOPPING_CHOICES):
            preferences_shopping_list_field.append(
                Div(
                    Div(
                        HTML(
                            '<input type="checkbox" class="form-checkbox" name="pref_shopping_list" id="cbx-'
                            + str(index + 1)
                            + '" value="'
                            + list_item[0]
                            + '" {% if "'
                            + list_item[0]
                            + '" in preferences_and_shopping_list %}checked{% endif %}><label for="cbx-'
                            + str(index + 1)
                            + '" class="fw-700">'
                            + list_item[1]
                            + "</label>"
                        ),
                        css_class="form-group m-0",
                    ),
                    css_class="col-12 col-md-12",
                )
            )

        self.helper.layout = Layout(
            Div(
                Div(
                    HTML(
                        """
                        <btn class='btn btn-solid-gold w-50' id='selectAllBtn'>Select All</btn>
            """
                    ),
                    css_class="col-12 align-items-center",
                ),
                Div(
                    Div(
                        *preferences_shopping_list_field,
                        css_class="form-row pl-3 pt-3 border-left-gray-80-1 mx-0",
                    ),
                    css_class="col-12",
                ),
                css_class="row",
            ),
            Div(FormActions(extract_button), css_class="col-md-12 mb-3"),
        )


class EditTripDetailsForm(forms.Form):
    first_name = forms.CharField(label="First Name")
    last_name = forms.CharField(label="Last Name")
    email = forms.EmailField(label="Email Address")
    # embark_date = forms.DateField()
    # disembark_date = forms.DateField()
    embark_time = forms.CharField(
        label="Time", widget=forms.TextInput(attrs={"type": "time"})
    )
    disembark_time = forms.CharField(
        label="Time", widget=forms.TextInput(attrs={"type": "time"}), required=False
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.helper = FormHelper(self)
        self.helper.form_id = "id-editTripDetailsForm"
        self.helper.form_class = "row"
        self.helper.form_method = "post"
        self.helper.label_class = "form-label"

        update_changes = Submit(
            "submit",
            "Update Changes",
        )
        update_changes.field_classes = "btn btn-solid-gold w-100"

        cancel_button = Div(
            Div(
                HTML(
                    """
                    <a href="{% url 'charter:trip_details' charter_id=charter.pk %}" class="btn btn-outline-secondary w-100">Cancel</a>
                    """
                ),
                css_class="form-group",
            ),
            css_class="col-md-5 mb-3",
        )

        apa_budget_field = Div(
            Div(
                Div(
                    HTML(
                        """
                    <span class="txt-color-dark-80 position-absolute fs-16 fw-700" style="bottom:30px">$</span>
                            <label for="" class="form-label">Amount</label>
                            <input type="text" class="form-control currency-amount" id="inlineFormInputGroup" name="apa_budget" placeholder="0.00" size="8" value="{{apa_budget}}" required>
                    """
                    ),
                    css_class="form-group",
                ),
                css_class="col-6 col-sm-9",
            ),
            Div(
                Div(
                    HTML(
                        """
                    <label for="" class="form-label"></label>
                    <select class="currency-selector form-select" name="currency">
                        <option data-symbol="$" data-placeholder="0.00" value="USD" {% if currency == 'USD' %}selected{% endif %}>$ USD
                        </option>
                        <option data-symbol="€" data-placeholder="0.00" value="EURO" {% if currency == 'EURO' %}selected{% endif %}>€ Euro</option>
                        <option data-symbol="£" data-placeholder="0.00" value="POUNDS" {% if currency == 'POUNDS' %}selected{% endif %}>£ British Pounds</option>
                    </select>
                    """
                    ),
                    css_class="form-group",
                ),
                css_class="col",
            ),
            css_class="form-row pl-3 pt-3 border-left-gray-80-1 mx-0",
        )

        embark_date_field = Div(
            HTML(
                """
                <div class="form-group">
                    <label for="" class="form-label">Date</label>
                    <div class="input-group align-items-center border-bottom-secondary-1">
                        <input type="text" class="form-control datepicker border-0" value="{{ embark_date }}" name="embark_date" placeholder="DD MM YYYY">
                        <div class="input-group-append">
                            <i class="far fa-calendar txt-color-white"></i>
                        </div>
                    </div>
                </div>
                """
            ),
            css_class="col-12 col-md-4",
        )

        embark_time_field = Div(
            HTML(
                """
                <label for="" class="form-label">Yacht Embark Time</label>
                <div class="input-group align-items-center border-bottom-secondary-1">
                    <input type="text" class="form-control timepicker border-0" name="embark_time" value="{{ embark_time }}" placeholder="HH:MM">
                    <div class="input-group-append">
                        <i class="far fa-clock txt-color-white"></i>
                    </div>
                </div>
                """
            ),
            css_class="col-12 col-md-4",
        )

        disembark_date_field = Div(
            HTML(
                """
                <div class="form-group">
                    <label for="" class="form-label">Date</label>
                    <div class="input-group align-items-center border-bottom-secondary-1">
                        <input type="text" class="form-control datepicker border-0" value="{{ disembark_date }}" name="disembark_date" placeholder="DD MM YYYY">
                        <div class="input-group-append">
                            <i class="far fa-calendar txt-color-white"></i>
                        </div>
                    </div>
                </div>
                """
            ),
            css_class="col-12 col-md-4",
        )

        disembark_time_field = Div(
            HTML(
                """
                <label for="" class="form-label">Yacht Disembark Time</label>
                <div class="input-group align-items-center border-bottom-secondary-1">
                    <input type="text" class="form-control timepicker border-0" name="disembark_time" value="{{ disembark_time }}" placeholder="HH:MM">
                    <div class="input-group-append">
                        <i class="far fa-clock txt-color-white"></i>
                    </div>
                </div>
                """
            ),
            css_class="col-12 col-md-4",
        )

        self.helper.layout = Layout(
            Div(
                Div(
                    HTML(
                        """
                    <span class='fs-11 fw-700 txt-color-gray text-uppercase'>
                        Principal Info
                    </span>
                    """
                    ),
                    Div(
                        Div(
                            Field(
                                "first_name",
                                placeholder="Enter First Name",
                            ),
                            css_class="col-12 col-md-6",
                        ),
                        Div(
                            Field(
                                "last_name",
                                placeholder="Enter Last Name",
                            ),
                            css_class="col-12 col-md-6",
                        ),
                        Div(
                            Field(
                                "email",
                                placeholder="Enter Email Address",
                            ),
                            css_class="col-12 col-md-12",
                        ),
                        css_class="form-row pl-3 pt-3 border-left-gray-80-1 mx-0",
                    ),
                    css_class="w-100 mb-4",
                ),
                css_class="col-12",
            ),
            Div(
                Div(
                    HTML(
                        """
                    <span class="fs-18 fw-700 txt-color-white text-uppercase">
                        Set APA Budget
                    </span>
                    """
                    ),
                    apa_budget_field,
                    css_class="w-100",
                ),
                css_class="col-12",
            ),
            Div(
                Div(
                    HTML(
                        """
                        <span class="fs-11 fw-700 txt-color-gray text-uppercase">
                            Yacht  Trip Embark
                        </span>
                    """
                    ),
                    Div(
                        Div(
                            HTML(
                                """
                                <label for="" class="form-label">Embark Location</label>
                                <input type="text" class="form-control textInput" value="{{ charter.embark_name_of_dock|default_if_none:"" }}" id="id_embark_name_of_dock" name="embark_name_of_dock" placeholder="Name of Dock / Yacht Club / Marina" required>
                                """
                            ),
                            css_class="col-12 col-md-12",
                        ),
                        Div(
                            HTML(
                                '<input type="text" class="form-control textInput" value="{{ charter.embark_city|default_if_none:"" }}" id="id_embark_city" name="embark_city" placeholder="City" required>'
                            ),
                            css_class="col-12 col-md-6",
                        ),
                        Div(
                            HTML(
                                '<input type="text" class="form-control textInput" value="{{ charter.embark_country|default_if_none:"" }}" id="id_embark_country" name="embark_country" placeholder="Country" required>'
                            ),
                            css_class="col-12 col-md-6",
                        ),
                        Div(
                            HTML(
                                '<textarea class="form-control mt-2" rows="2" cols="20" id="id_embark_additional_info" name="embark_additional_info" placeholder="Additional Info">{{ charter.embark_additional_info|default_if_none:"" }}</textarea>'
                            ),
                            css_class="col-12 col-md-12",
                        ),
                        embark_date_field,
                        Div(css_class="col-12 col-md-8"),
                        embark_time_field,
                        Div(css_class="col-12 col-md-8"),
                        css_class="form-row pl-3 pt-3 border-left-gray-80-1 mx-0",
                    ),
                    css_class="w-100 mb-4",
                ),
                Div(
                    HTML(
                        """
                        <span class="fs-11 fw-700 txt-color-gray text-uppercase">
                            Yacht  Trip Disembark
                        </span>
                        """
                    ),
                    Div(
                        Div(
                            HTML(
                                """
                                <label for="" class="form-label">Disembark Location</label>
                                <input type="text" class="form-control textInput" value="{{ charter.disembark_name_of_dock|default_if_none:"" }}" id="id_disembark_name_of_dock" name="disembark_name_of_dock" placeholder="Name of Dock / Yacht Club / Marina" required>
                                """
                            ),
                            css_class="col-12 col-md-12",
                        ),
                        Div(
                            HTML(
                                '<input type="text" class="form-control textInput" value="{{ charter.disembark_city|default_if_none:"" }}" id="id_disembark_city" name="disembark_city" placeholder="City" required>'
                            ),
                            css_class="col-12 col-md-6",
                        ),
                        Div(
                            HTML(
                                '<input type="text" class="form-control textInput" value="{{ charter.disembark_country|default_if_none:"" }}" id="id_disembark_country" name="disembark_country" placeholder="Country" required>'
                            ),
                            css_class="col-12 col-md-6",
                        ),
                        Div(
                            HTML(
                                '<textarea class="form-control mt-2" rows="2" cols="20" id="id_disembark_additional_info" name="disembark_additional_info" placeholder="Additional Info">{{ charter.disembark_additional_info|default_if_none:"" }}</textarea>'
                            ),
                            css_class="col-12 col-md-12",
                        ),
                        disembark_date_field,
                        Div(css_class="col-12 col-md-8"),
                        disembark_time_field,
                        Div(css_class="col-12 col-md-8"),
                        css_class="form-row pl-3 pt-3 border-left-gray-80-1 mx-0",
                    ),
                    css_class="w-100 mb-4",
                ),
                Div(
                    Div(FormActions(update_changes), css_class="col-md-5 mb-3"),
                    cancel_button,
                    css_class="form-row px-0 mx-0",
                ),
                css_class="col-12",
            ),
        )
