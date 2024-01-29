from django import forms
from django.urls import reverse

from crispy_forms.bootstrap import FormActions
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit, Layout, Field, HTML, Div
from crispy_forms.utils import TEMPLATE_PACK

from charter.models import MealAndRoomPreferences
from preferences.constants import (
    BREAD,
    BREAKFAST,
    CANAPES_TIME_CHOICES,
    CANAPES_TYPES,
    CHEESE,
    COFFEE_SELECTIONS,
    DESSERT,
    DIETARY_RESTRICTIONS,
    DINNER,
    FISH_SHELLFISH,
    GENERAL_CUISINE,
    INTERNATIONAL_SHIRT_SIZING,
    INTERNATIONAL_SHOE_SIZING,
    JUICE_SELECTIONS,
    LUNCH,
    MEAT,
    MID_AFTERNOON_SNACKS,
    MID_MORNING_SNACKS,
    MILK_SELECTIONS,
    OTHER_SERVICES,
    SALAD,
    SHIRT_SIZE,
    SHIRT_SIZING,
    SHOE_SIZING,
    SODAS_MIXERS_SELECTIONS,
    SOUP,
    TEA_SELECTIONS,
    WATER_SELECTIONS,
    ADD_ONS_SELECTIONS,
)
from preferences.helpers import generate_html_from_alcohol_dict
from preferences.models import (
    DietaryRestrictionChoices,
    KidsChoices,
    LongJetPreferenceSheet,
    ShortJetPreferenceSheet,
)


class CustomInlineCheckboxes(Field):
    """
    Layout object for rendering checkboxes inline::
    InlineCheckboxes('field_name')
    """

    template = "preferences/partials/custom_checkboxselectmultiple_inline.html"

    def render(self, form, form_style, context, template_pack=TEMPLATE_PACK, **kwargs):
        return super().render(
            form,
            form_style,
            context,
            template_pack=template_pack,
            extra_context={"inline_class": "inline"},
        )


class FoodPreferencesForm(forms.Form):
    general_cuisine = forms.MultipleChoiceField(
        label=" ",
        choices=GENERAL_CUISINE,
        widget=forms.widgets.CheckboxSelectMultiple,
    )
    general_cuisine_notes = forms.CharField(
        widget=forms.Textarea(
            attrs={"rows": 1, "cols": 20, "placeholder": "Type Here"}
        ),
        label="Note to Chef",
        required=False,
    )
    fish_and_shellfish = forms.MultipleChoiceField(
        label=" ",
        choices=FISH_SHELLFISH,
        widget=forms.widgets.CheckboxSelectMultiple,
    )
    fish_and_shellfish_notes = forms.CharField(
        widget=forms.Textarea(
            attrs={"rows": 1, "cols": 20, "placeholder": "Type Here"}
        ),
        label="Note to Chef",
        required=False,
    )
    meat = forms.MultipleChoiceField(
        label=" ",
        choices=MEAT,
        widget=forms.widgets.CheckboxSelectMultiple,
    )
    meat_notes = forms.CharField(
        widget=forms.Textarea(
            attrs={"rows": 1, "cols": 20, "placeholder": "Type Here"}
        ),
        label="Note to Chef",
        required=False,
    )
    bread = forms.MultipleChoiceField(
        label=" ",
        choices=BREAD,
        widget=forms.widgets.CheckboxSelectMultiple,
    )
    bread_notes = forms.CharField(
        widget=forms.Textarea(
            attrs={"rows": 1, "cols": 20, "placeholder": "Type Here"}
        ),
        label="Note to Chef",
        required=False,
    )
    soup = forms.MultipleChoiceField(
        label=" ",
        choices=SOUP,
        widget=forms.widgets.CheckboxSelectMultiple,
    )
    soup_notes = forms.CharField(
        widget=forms.Textarea(
            attrs={"rows": 1, "cols": 20, "placeholder": "Type Here"}
        ),
        label="Note to Chef",
        required=False,
    )
    salad = forms.MultipleChoiceField(
        label=" ",
        choices=SALAD,
        widget=forms.widgets.CheckboxSelectMultiple,
    )
    salad_notes = forms.CharField(
        widget=forms.Textarea(
            attrs={"rows": 1, "cols": 20, "placeholder": "Type Here"}
        ),
        label="Note to Chef",
        required=False,
    )
    cheese = forms.MultipleChoiceField(
        label=" ",
        choices=CHEESE,
        widget=forms.widgets.CheckboxSelectMultiple,
    )
    cheese_notes = forms.CharField(
        widget=forms.Textarea(
            attrs={"rows": 1, "cols": 20, "placeholder": "Type Here"}
        ),
        label="Note to Chef",
        required=False,
    )
    kids_meals = forms.MultipleChoiceField(
        label=" ",
        choices=KidsChoices.choices,
        widget=forms.widgets.CheckboxSelectMultiple,
        required=False,
    )
    kids_allergies = forms.CharField(
        widget=forms.Textarea(
            attrs={"rows": 2, "cols": 20, "placeholder": "Type Here"}
        ),
        label="Kids Allergies",
        required=False,
    )
    kids_meals_notes = forms.CharField(
        widget=forms.Textarea(
            attrs={"rows": 1, "cols": 20, "placeholder": "Type Here"}
        ),
        label="Note to Chef",
        required=False,
    )
    dessert = forms.MultipleChoiceField(
        label=" ",
        choices=DESSERT,
        widget=forms.widgets.CheckboxSelectMultiple,
    )
    dessert_notes = forms.CharField(
        widget=forms.Textarea(
            attrs={"rows": 1, "cols": 20, "placeholder": "Type Here"}
        ),
        label="Note to Chef",
        required=False,
    )

    def __init__(self, *args, **kwargs):
        view = ""
        if "view" in kwargs:
            view = kwargs.pop("view")
        super().__init__(*args, **kwargs)

        self.helper = FormHelper(self)
        self.helper.form_id = "id-foodPreferencesForm"
        self.helper.form_class = "form-container-profile ml-0"
        self.helper.form_method = "post"
        self.helper.label_class = "form-label"

        save_button = Submit(
            "submit",
            "Save",
        )
        self.form_action = "preferences:yacht_food_preference"
        ### Form customization for reuseability
        if view == "onboarding":
            save_button = Submit(
                "submit",
                "Save & Continue",
            )
            self.form_action = "guests:yacht_food_onboarding"

        save_button.field_classes = "btn btn-solid-gold w-100"

        general_cuisine_fields = Div(
            Div(
                HTML(
                    """
                <label class="form-label">General Cuisine</label>
                """
                ),
                Div(
                    CustomInlineCheckboxes("general_cuisine"),
                    Div(Field("general_cuisine_notes"), css_class="col-12 mt-3"),
                    css_class="form-row mt-3",
                ),
                css_class="form-group pt-0",
            ),
            css_class="col-12",
        )
        fish_shellfish_fields = Div(
            Div(
                HTML(
                    """
                <label class="form-label">Fish and Shellfish</label>
                """
                ),
                Div(
                    CustomInlineCheckboxes("fish_and_shellfish"),
                    Div(Field("fish_and_shellfish_notes"), css_class="col-12 mt-3"),
                    css_class="form-row mt-3",
                ),
                css_class="form-group pt-0",
            ),
            css_class="col-12 mt-4",
        )
        meat_fields = Div(
            Div(
                HTML(
                    """
                <label class="form-label">Meat</label>
                """
                ),
                Div(
                    CustomInlineCheckboxes("meat"),
                    Div(Field("meat_notes"), css_class="col-12 mt-3"),
                    css_class="form-row mt-3",
                ),
                css_class="form-group pt-0",
            ),
            css_class="col-12 mt-4",
        )
        bread_fields = Div(
            Div(
                HTML(
                    """
                <label class="form-label">Bread</label>
                """
                ),
                Div(
                    CustomInlineCheckboxes("bread"),
                    Div(Field("bread_notes"), css_class="col-12 mt-3"),
                    css_class="form-row mt-3",
                ),
                css_class="form-group pt-0",
            ),
            css_class="col-12 mt-4",
        )
        soup_fields = Div(
            Div(
                HTML(
                    """
                <label class="form-label">Soup</label>
                """
                ),
                Div(
                    CustomInlineCheckboxes("soup"),
                    Div(Field("soup_notes"), css_class="col-12 mt-3"),
                    css_class="form-row mt-3",
                ),
                css_class="form-group pt-0",
            ),
            css_class="col-12 mt-4",
        )
        salad_fields = Div(
            Div(
                HTML(
                    """
                <label class="form-label">Salad</label>
                """
                ),
                Div(
                    CustomInlineCheckboxes("salad"),
                    Div(Field("salad_notes"), css_class="col-12 mt-3"),
                    css_class="form-row mt-3",
                ),
                css_class="form-group pt-0",
            ),
            css_class="col-12 mt-4",
        )
        cheese_fields = Div(
            Div(
                HTML(
                    """
                <label class="form-label">Cheese</label>
                """
                ),
                Div(
                    CustomInlineCheckboxes("cheese"),
                    Div(Field("cheese_notes"), css_class="col-12 mt-3"),
                    css_class="form-row mt-3",
                ),
                css_class="form-group pt-0",
            ),
            css_class="col-12 mt-4",
        )
        dessert_fields = Div(
            Div(
                HTML(
                    """
                <label class="form-label">Dessert</label>
                """
                ),
                Div(
                    CustomInlineCheckboxes("dessert"),
                    Div(Field("dessert_notes"), css_class="col-12 mt-3"),
                    css_class="form-row mt-3",
                ),
                css_class="form-group pt-0",
            ),
            css_class="col-12 mt-4",
        )
        kids_meals_fields = Div(
            Div(
                HTML(
                    """
                <label for="" class="form-label">Kids Meals</label>
                """
                ),
                Div(
                    CustomInlineCheckboxes("kids_meals"),
                    Div(Field("kids_meals_notes"), css_class="col-12 mt-3"),
                    css_class="form-row mt-3",
                ),
                css_class="form-group pt-0",
            ),
            css_class="col-12",
        )
        kids_allergies_fields = Div(
            Field("kids_allergies"),
            css_class="col-12 mt-3",
        )

        self.helper.layout = Layout(
            Div(
                Div(
                    Div(
                        HTML(
                            """
                            <span class="fs-18 fw-700 txt-color-white text-uppercase">
                                Food
                            </span>
                            """
                        ),
                        Div(
                            general_cuisine_fields,
                            fish_shellfish_fields,
                            meat_fields,
                            bread_fields,
                            soup_fields,
                            salad_fields,
                            cheese_fields,
                            dessert_fields,
                            kids_allergies_fields,
                            kids_meals_fields,
                            css_class="form-row pl-3 pt-3 border-left-gray-80-1 mx-0",
                        ),
                        css_class="w-100 mb-4",
                    ),
                    css_class="col-12",
                ),
                Div(FormActions(save_button), css_class="col-md-5 mb-3"),
                # skip_button,
                css_class="row px-3",
            ),
        )


class MealAndRoomPreferencesForm(forms.Form):
    breakfast_time = forms.ChoiceField(
        choices=MealAndRoomPreferences.time_choices,
        label="Select Breakfast Time",
        widget=forms.widgets.Select,
    )
    breakfast_selection = forms.MultipleChoiceField(
        label=" ",
        choices=BREAKFAST,
        widget=forms.widgets.CheckboxSelectMultiple,
        required=True,
    )
    breakfast_note = forms.CharField(
        widget=forms.Textarea(
            attrs={"rows": 1, "cols": 20, "placeholder": "Type Here"}
        ),
        label="Note to Chef",
        required=False,
    )
    lunch_time = forms.ChoiceField(
        choices=MealAndRoomPreferences.time_choices,
        label="Select Lunch Time",
        widget=forms.widgets.Select,
    )
    lunch_selection = forms.MultipleChoiceField(
        label=" ",
        choices=LUNCH,
        widget=forms.widgets.CheckboxSelectMultiple,
    )
    lunch_note = forms.CharField(
        widget=forms.Textarea(
            attrs={"rows": 1, "cols": 20, "placeholder": "Type Here"}
        ),
        label="Note to Chef",
        required=False,
    )
    dinner_time = forms.ChoiceField(
        choices=MealAndRoomPreferences.time_choices,
        label="Select Dinner Time",
        widget=forms.widgets.Select,
    )
    dinner_selection = forms.MultipleChoiceField(
        label=" ",
        choices=DINNER,
        widget=forms.widgets.CheckboxSelectMultiple,
    )
    dinner_note = forms.CharField(
        widget=forms.Textarea(
            attrs={"rows": 1, "cols": 20, "placeholder": "Type Here"}
        ),
        label="Note to Chef",
        required=False,
    )
    canapes_time = forms.ChoiceField(
        choices=CANAPES_TIME_CHOICES,
        label="Select Canapes Time",
        widget=forms.widgets.Select,
    )
    dietary_restrictions_notes = forms.CharField(
        widget=forms.Textarea(
            attrs={"rows": 1, "cols": 20, "placeholder": "Type Here"}
        ),
        label="Please note any food preference details here",
        required=False,
    )
    dietary_restrictions_other_notes = forms.CharField(
        widget=forms.Textarea(attrs={"rows": 2, "cols": 20}),
        label="Other",
        required=False,
    )

    def __init__(self, *args, **kwargs):
        view = ""
        if "view" in kwargs:
            view = kwargs.pop("view")
        super().__init__(*args, **kwargs)

        self.helper = FormHelper(self)
        self.helper.form_id = "id-mealAndRoomPreferencesForm"
        self.helper.form_class = "form-container-profile ml-0"
        self.helper.form_method = "post"
        self.helper.label_class = "form-label"

        ### Form customization for reuseability
        if view == "onboarding":
            save_button = Submit(
                "submit",
                "Save & Continue",
            )
            self.form_action = "guests:onboarding_meal_and_room"

        save_button = Submit("submit", "Save & Continue", css_id="submit_meal")
        save_button.field_classes = "btn btn-solid-gold w-100"
        dietary_restrictions_field = []
        dietary_restrictions_other_field = []
        for index, list_item in enumerate(DIETARY_RESTRICTIONS):
            if list_item[0] != "OTHER":
                dietary_restrictions_field.append(
                    Div(
                        HTML(
                            '<input type="radio" class="form-radio" name="dietary_restrictions" id="dt-cbx-'
                            + str(index + 1)
                            + '" value="'
                            + list_item[0]
                            + '" {% if "'
                            + list_item[0]
                            + '" in dietary_restrictions %}checked{% endif %}><label for="dt-cbx-'
                            + str(index + 1)
                            + '" class="form-radio-label fw-700" required>'
                            + list_item[1]
                            + "</label>"
                        ),
                        css_class="w-100 mb-3",
                    )
                )
            else:
                dietary_restrictions_other_field.append(
                    Div(
                        HTML(
                            '<input type="radio" class="form-radio" name="dietary_restrictions" id="dt-cbx-'
                            + str(index + 1)
                            + '" value="'
                            + list_item[0]
                            + '" {% if "'
                            + list_item[0]
                            + '" in dietary_restrictions %}checked{% endif %}><label for="dt-cbx-'
                            + str(index + 1)
                            + '" class="form-radio-label fw-700">'
                            + list_item[1]
                            + "</label>"
                        ),
                        css_class="w-100 mb-3",
                    )
                )

        dietary_restrictions_main_field = Div(
            Div(
                *dietary_restrictions_field,
                HTML(
                    """
                    <div class="error_dietary_restrictions w-100 custom-control custom-checkbox custom-control-inline mt-3" style="display: none">
                        <input type="checkbox" class="custom-control-input is-invalid">
                        <p id="" class="invalid-feedback">
                        <strong>This field is required.</strong></p>
                    </div>
                    """
                ),
                css_class="col-12 col-sm-6",
            ),
            Div(
                *dietary_restrictions_other_field,
                Field("dietary_restrictions_other_notes", placeholder="Type here"),
                css_class="col-12 col-sm-6",
            ),
            Div(
                Field("dietary_restrictions_notes", placeholder="Type here"),
                css_class="col-12",
            ),
            css_class="form-row mt-4",
        )

        skip_button = None
        if view != "onboarding":
            skip_button = Div(
                Div(
                    HTML(
                        """
                        <a href="{% url 'preferences:diet_services_sizing' %}" class="btn btn-outline-secondary w-100">Skip</a>
                        """
                    ),
                    css_class="form-group",
                ),
                css_class="col-md-5 mb-3",
            )

        # FIELDS
        breakfast_time = Div(
            Div(
                Field(
                    "breakfast_time",
                    placeholder="Select Breakfast Time",
                    css_class="form-select",
                ),
                css_class="col-md-6",
            ),
            css_class="form-row mb-5",
        )
        breakfast_fields = Div(
            CustomInlineCheckboxes("breakfast_selection"),
            Div(Field("breakfast_note"), css_class="col-12 mt-3"),
            css_class="form-row mt-3",
        )
        lunch_time = Div(
            Div(
                Field(
                    "lunch_time",
                    placeholder="Select Lunch Time",
                    css_class="form-select",
                ),
                css_class="col-md-6",
            ),
            css_class="form-row mb-5",
        )
        lunch_fields = Div(
            CustomInlineCheckboxes("lunch_selection"),
            Div(Field("lunch_note"), css_class="col-12 mt-3"),
            css_class="form-row mt-3",
        )
        dinner_time = Div(
            Div(
                Field(
                    "dinner_time",
                    placeholder="Select Dinner Time",
                    css_class="form-select",
                ),
                css_class="col-md-6",
            ),
            css_class="form-row mb-5",
        )
        dinner_fields = Div(
            CustomInlineCheckboxes("dinner_selection"),
            Div(Field("dinner_note"), css_class="col-12 mt-3"),
            css_class="form-row mt-3",
        )
        canapes_time = Div(
            Div(
                Field(
                    "canapes_time",
                    placeholder="Select Canapes Time",
                    css_class="form-select",
                ),
                css_class="col-md-6",
            ),
            css_class="form-row mb-3",
        )
        canapes_field = []
        for index, list_item in enumerate(CANAPES_TYPES):
            canapes_field.append(
                Div(
                    HTML(
                        '<input type="radio" class="form-radio" name="canapes_selection" id="cnp-rd-'
                        + str(index + 1)
                        + '" value="'
                        + list_item[0]
                        + '" {% if "'
                        + list_item[0]
                        + '" in canapes_selection %}checked{% endif %}><label for="cnp-rd-'
                        + str(index + 1)
                        + '" class="form-radio-label fw-700">'
                        + list_item[1]
                        + "</label>"
                    ),
                    css_class="col-12 col-sm-6 mb-3",
                )
            )
        mid_morning_snack_field = []
        for index, list_item in enumerate(MID_MORNING_SNACKS):
            mid_morning_snack_field.append(
                Div(
                    HTML(
                        '<input type="radio" class="form-radio" name="midmorning_snacks" id="id_midmorning_snacks_'
                        + str(index + 1)
                        + '" value="'
                        + list_item[0]
                        + '" {% if "'
                        + list_item[0]
                        + '" in midmorning_snacks %}checked{% endif %}><label for="id_midmorning_snacks_'
                        + str(index + 1)
                        + '" class="form-radio-label fw-700">'
                        + list_item[1]
                        + "</label>"
                    ),
                    css_class="col-12 col-sm-6 mb-3",
                )
            )
        mid_afternoon_snack_field = []
        for index, list_item in enumerate(MID_AFTERNOON_SNACKS):
            mid_afternoon_snack_field.append(
                Div(
                    HTML(
                        '<input type="radio" class="form-radio" name="midafternoon_snacks" id="id_midafternoon_snacks_'
                        + str(index + 1)
                        + '" value="'
                        + list_item[0]
                        + '" {% if "'
                        + list_item[0]
                        + '" in midafternoon_snacks %}checked{% endif %}><label for="id_midafternoon_snacks_'
                        + str(index + 1)
                        + '" class="form-radio-label fw-700">'
                        + list_item[1]
                        + "</label>"
                    ),
                    css_class="col-12 col-sm-6 mb-3",
                )
            )

        self.helper.layout = Layout(
            Div(
                Div(
                    Div(
                        HTML(
                            """
                            <span class="fs-18 fw-700 txt-color-white text-uppercase">
                                Dietary Restrictions
                            </span>
                            """
                        ),
                        Div(
                            Div(
                                Div(
                                    Div(
                                        Div(
                                            HTML(
                                                """
                                                <span class="fs-14 txt-color-gold d-table mt-1 fw-700">Please indicate if you are....</span>
                                                """
                                            ),
                                            css_class="col-md-6",
                                        ),
                                        css_class="form-row",
                                    ),
                                    dietary_restrictions_main_field,
                                    css_class="form-group py-0",
                                ),
                                css_class="col-12",
                            ),
                            css_class="form-row pl-3 pt-3 border-left-gray-80-1 mx-0",
                        ),
                        css_class="w-100 mb-4",
                    ),
                    Div(
                        Div(
                            HTML(
                                """
                                <span class="fs-18 fw-700 txt-color-white text-uppercase">Meal Times & Types</span>
                                <span class="fs-14 txt-color-gray d-table">What general time would you like this to be served?</span>
                                """
                            ),
                            css_class="col-12",
                        ),
                        css_class="form-row mb-3",
                    ),
                    Div(
                        HTML(
                            """
                            <span class="fs-18 fw-700 txt-color-white text-uppercase">
                                Breakfast
                            </span>
                            """
                        ),
                        Div(
                            Div(
                                Div(
                                    breakfast_time,
                                    breakfast_fields,
                                    css_class="form-group pt-0",
                                ),
                                css_class="col-12",
                            ),
                            css_class="form-row pl-3 pt-3 border-left-gray-80-1 mx-0",
                        ),
                        css_class="w-100 mb-4",
                    ),
                    Div(
                        HTML(
                            """
                            <span class="fs-18 fw-700 txt-color-white text-uppercase">
                                Lunch
                            </span>
                            """
                        ),
                        Div(
                            Div(
                                Div(
                                    lunch_time,
                                    lunch_fields,
                                    css_class="form-group pt-0",
                                ),
                                css_class="col-12",
                            ),
                            css_class="form-row pl-3 pt-3 border-left-gray-80-1 mx-0",
                        ),
                        css_class="w-100 mb-4",
                    ),
                    Div(
                        HTML(
                            """
                            <span class="fs-18 fw-700 txt-color-white text-uppercase">
                                Dinner
                            </span>
                            """
                        ),
                        Div(
                            Div(
                                Div(
                                    dinner_time,
                                    dinner_fields,
                                    css_class="form-group pt-0",
                                ),
                                css_class="col-12",
                            ),
                            css_class="form-row pl-3 pt-3 border-left-gray-80-1 mx-0",
                        ),
                        css_class="w-100 mb-4",
                    ),
                    Div(
                        HTML(
                            """
                            <span class="fs-18 fw-700 txt-color-white text-uppercase">
                                Canapes
                            </span>
                            """
                        ),
                        Div(
                            Div(
                                Div(
                                    canapes_time,
                                    Div(
                                        *canapes_field,
                                        HTML(
                                            """
                                            <div class="error_canapes_selection w-100 custom-control custom-checkbox custom-control-inline mt-3" style="display: none">
                                                <input type="checkbox" class="custom-control-input is-invalid">
                                                <p id="" class="invalid-feedback">
                                                <strong>This field is required.</strong></p>
                                            </div>
                                            """
                                        ),
                                        css_class="form-row mt-3",
                                    ),
                                    css_class="form-group pt-0 mb-0",
                                ),
                                css_class="col-12",
                            ),
                            css_class="form-row pl-3 pt-3 border-left-gray-80-1 mx-0",
                        ),
                        css_class="w-100 mb-4",
                    ),
                    Div(
                        HTML(
                            """
                            <span class="fs-18 fw-700 txt-color-white text-uppercase">
                                Mid-Morning Snack
                            </span>
                            """
                        ),
                        Div(
                            Div(
                                Div(
                                    Div(
                                        Div(
                                            HTML(
                                                """
                                                <label for="" class="form-label">Select Mid-morning Snack</label>
                                                """
                                            ),
                                            css_class="col-md-6",
                                        ),
                                        css_class="form-row mb-2",
                                    ),
                                    Div(
                                        *mid_morning_snack_field,
                                        HTML(
                                            """
                                            <div class="error_midmorning_snacks w-100 custom-control custom-checkbox custom-control-inline mt-3" style="display: none">
                                                <input type="checkbox" class="custom-control-input is-invalid">
                                                <p id="" class="invalid-feedback">
                                                <strong>This field is required.</strong></p>
                                            </div>
                                            """
                                        ),
                                        css_class="form-row mt-3",
                                    ),
                                    css_class="form-group pt-0 mb-0",
                                ),
                                css_class="col-12",
                            ),
                            css_class="form-row pl-3 pt-3 border-left-gray-80-1 mx-0",
                        ),
                        css_class="w-100 mb-4",
                    ),
                    Div(
                        HTML(
                            """
                            <span class="fs-18 fw-700 txt-color-white text-uppercase">
                                Mid-Afternoon Snack
                            </span>
                            """
                        ),
                        Div(
                            Div(
                                Div(
                                    Div(
                                        Div(
                                            HTML(
                                                """
                                                <label for="" class="form-label">Select Mid-Afternoon Snack</label>
                                                """
                                            ),
                                            css_class="col-md-6",
                                        ),
                                        css_class="form-row mb-2",
                                    ),
                                    Div(
                                        *mid_afternoon_snack_field,
                                        HTML(
                                            """
                                            <div class="error_midafternoon_snacks w-100 custom-control custom-checkbox custom-control-inline mt-3" style="display: none">
                                                <input type="checkbox" class="custom-control-input is-invalid">
                                                <p id="" class="invalid-feedback">
                                                <strong>This field is required.</strong></p>
                                            </div>
                                            """
                                        ),
                                        css_class="form-row mt-3",
                                    ),
                                    css_class="form-group pt-0 mb-0",
                                ),
                                css_class="col-12",
                            ),
                            css_class="form-row pl-3 pt-3 border-left-gray-80-1 mx-0",
                        ),
                        css_class="w-100 mb-4",
                    ),
                    css_class="col-12",
                ),
                Div(FormActions(save_button), css_class="col-md-5 mb-3"),
                skip_button,
                css_class="row mt",
            ),
        )


class DietServicesSizesForm(forms.Form):
    preferred_room_temperature = forms.CharField(
        label="What is your preferred room temperature?", required=False
    )
    favorite_flowers = forms.CharField(
        label="What are your favorite flowers?",
        required=False,
        widget=forms.Textarea(
            attrs={"rows": 1, "cols": 20, "placeholder": "Roses, Lilies, etc.,."}
        ),
    )
    other_services_other_notes = forms.CharField(
        widget=forms.Textarea(attrs={"rows": 2, "cols": 20}),
        label="Other",
        required=False,
    )
    shoe_size = forms.IntegerField(label="Enter your shoe size")

    def __init__(self, *args, **kwargs):
        view = ""
        if "view" in kwargs:
            view = kwargs.pop("view")
        super().__init__(*args, **kwargs)

        self.helper = FormHelper(self)
        self.helper.form_id = "id-dietServicesSizesPreferencesForm"
        self.helper.form_class = "form-container-profile ml-0"
        self.helper.form_method = "post"
        self.helper.label_class = "form-label"

        save_button = Submit("submit", "Save & Continue", css_id="submit_diet")
        ### Form customization for reuseability
        if view == "onboarding":
            save_button = Submit(
                "submit",
                "Save & Continue",
            )
            self.form_action = "guests:onboarding_diet_services"

        save_button.field_classes = "btn btn-solid-gold w-100"

        skip_button = None
        if view != "onboarding":
            skip_button = Div(
                Div(
                    HTML(
                        """
                        <a href="{% url 'preferences:beverage_alcohol' %}" class="btn btn-outline-secondary w-100">Skip</a>
                        """
                    ),
                    css_class="form-group",
                ),
                css_class="col-md-5 mb-3",
            )

        preferred_room_temperature_field = Div(
            Field("preferred_room_temperature", placeholder="Type here"),
            css_class="col-12 mb-3",
        )

        other_services_field = []
        other_services_other_field = []
        for index, list_item in enumerate(OTHER_SERVICES):
            if list_item[0] != "OTHER":
                other_services_field.append(
                    Div(
                        HTML(
                            '<input type="checkbox" class="form-checkbox" name="other_services" id="os-cbx-'
                            + str(index + 1)
                            + '" value="'
                            + list_item[0]
                            + '" {% if "'
                            + list_item[0]
                            + '" in other_services %}checked{% endif %}><label for="os-cbx-'
                            + str(index + 1)
                            + '" class="form-radio-label fw-700">'
                            + list_item[1]
                            + "</label>"
                        ),
                        css_class="w-100 mb-3",
                    )
                )
            else:
                other_services_other_field.append(
                    Div(
                        HTML(
                            '<input type="checkbox" class="form-checkbox" name="other_services" id="os-cbx-'
                            + str(index + 1)
                            + '" value="'
                            + list_item[0]
                            + '" {% if "'
                            + list_item[0]
                            + '" in other_services %}checked{% endif %}><label for="os-cbx-'
                            + str(index + 1)
                            + '" class="form-radio-label fw-700">'
                            + list_item[1]
                            + "</label>"
                        ),
                        css_class="w-100 mb-3",
                    )
                )

        other_services_main_field = Div(
            Div(*other_services_field, css_class="col-12 col-sm-6"),
            Div(
                *other_services_other_field,
                Field("other_services_other_notes", placeholder="Type here"),
                css_class="col-12 col-sm-6",
            ),
            css_class="form-row mt-4",
        )

        shirt_sizing_field = []
        for index, list_item in enumerate(SHIRT_SIZING):
            shirt_sizing_field.append(
                Div(
                    HTML(
                        '<input type="radio" class="form-radio" name="shirt_sizing" id="id_shirt_sizing_'
                        + str(index + 1)
                        + '" value="'
                        + list_item[0]
                        + '" {% if "'
                        + list_item[0]
                        + '" in shirt_sizing %}checked{% endif %}><label for="id_shirt_sizing_'
                        + str(index + 1)
                        + '" class="txt-color-white form-radio-label fw-700">'
                        + list_item[1]
                        + "</label>"
                    ),
                    css_class="col-12 col-md-6",
                )
            )

        international_shirt_sizing_field = []
        for index, list_item in enumerate(INTERNATIONAL_SHIRT_SIZING):
            international_shirt_sizing_field.append(
                Div(
                    HTML(
                        '<input type="radio" class="form-radio" name="international_shirt_sizing" id="id_international_shirt_sizing_'
                        + str(index + 1)
                        + '" value="'
                        + list_item[0]
                        + '" {% if "'
                        + list_item[0]
                        + '" in international_shirt_sizing %}checked{% endif %}><label for="id_international_shirt_sizing_'
                        + str(index + 1)
                        + '" class="txt-color-white form-radio-label fw-700">'
                        + list_item[1]
                        + "</label>"
                    ),
                    css_class="col-12 col-md-6 mb-3",
                )
            )

        shirt_size_field = []
        for index, list_item in enumerate(SHIRT_SIZE):
            shirt_size_field.append(
                Div(
                    HTML(
                        '<input type="radio" class="form-radio" name="shirt_size" id="id_shirt_size_'
                        + str(index + 1)
                        + '" value="'
                        + list_item[0]
                        + '" {% if "'
                        + list_item[0]
                        + '" in shirt_size %}checked{% endif %}><label for="id_shirt_size_'
                        + str(index + 1)
                        + '" class="txt-color-white form-radio-label fw-700">'
                        + list_item[1]
                        + "</label>"
                    ),
                    css_class="col-12 col-md-6 mb-3",
                )
            )

        shoe_sizing_field = []
        for index, list_item in enumerate(SHOE_SIZING):
            shoe_sizing_field.append(
                Div(
                    HTML(
                        '<input type="radio" class="form-radio" name="shoe_sizing" id="id_shoe_sizing_'
                        + str(index + 1)
                        + '" value="'
                        + list_item[0]
                        + '" {% if "'
                        + list_item[0]
                        + '" in shoe_sizing %}checked{% endif %}><label for="id_shoe_sizing_'
                        + str(index + 1)
                        + '" class="txt-color-white form-radio-label fw-700">'
                        + list_item[1]
                        + "</label>"
                    ),
                    css_class="col-12 col-md-6",
                )
            )

        international_shoe_sizing_field = []
        for index, list_item in enumerate(INTERNATIONAL_SHOE_SIZING):
            international_shoe_sizing_field.append(
                Div(
                    HTML(
                        '<input type="radio" class="form-radio" name="international_shoe_sizing" id="id_international_shoe_sizing_'
                        + str(index + 1)
                        + '" value="'
                        + list_item[0]
                        + '" {% if "'
                        + list_item[0]
                        + '" in international_shoe_sizing %}checked{% endif %}><label for="id_international_shoe_sizing_'
                        + str(index + 1)
                        + '" class="txt-color-white form-radio-label fw-700">'
                        + list_item[1]
                        + "</label>"
                    ),
                    css_class="col-12 col-md-6 mb-3",
                )
            )

        self.helper.layout = Layout(
            Div(
                Div(
                    Div(
                        HTML(
                            """
                            <span class="fs-18 fw-700 txt-color-white text-uppercase">
                                Room
                            </span>
                            """
                        ),
                        Div(
                            preferred_room_temperature_field,
                            Div(
                                Div(
                                    Div(
                                        Div(
                                            Field(
                                                "favorite_flowers",
                                            ),
                                            css_class="col-md-12",
                                        ),
                                        css_class="form-row mb-2",
                                    ),
                                    css_class="form-group pt-0 mb-0",
                                ),
                                css_class="col-12",
                            ),
                            Div(
                                Div(
                                    HTML(
                                        """
                                        <span class="fs-14 txt-color-gold">Other Services</span>
                                        <span class="fs-14 txt-color-gray d-table mt-1">What other services would you be interested in for this trip?</span>
                                        """
                                    ),
                                    other_services_main_field,
                                    css_class="form-group py-0",
                                ),
                                css_class="col-12 mb-3",
                            ),
                            css_class="form-row pl-3 pt-3 border-left-gray-80-1 mx-0",
                        ),
                        css_class="w-100 mb-4",
                    ),
                    Div(
                        HTML(
                            """
                            <span class="fs-18 fw-700 txt-color-white text-uppercase">
                                Shirt Sizing
                            </span>
                            """
                        ),
                        Div(
                            Div(
                                Div(
                                    HTML(
                                        """
                                        <label for="" class="form-label">Please select your shirt size.</label>
                                        """
                                    ),
                                    css_class="form-group py-0",
                                ),
                                css_class="col-12 mb-3",
                            ),
                            Div(
                                Div(
                                    Div(
                                        HTML(
                                            """
                                            <span class="txt-color-gray">Preferred Sizing</span>
                                            """
                                        ),
                                        css_class="col-12 mb-3",
                                    ),
                                    *shirt_sizing_field,
                                    HTML(
                                        """
                                        <div class="error_shirt_sizing w-100 custom-control custom-checkbox custom-control-inline mt-3" style="display: none">
                                            <input type="checkbox" class="custom-control-input is-invalid">
                                            <p id="" class="invalid-feedback">
                                            <strong>This field is required.</strong></p>
                                        </div>
                                        """
                                    ),
                                    css_class="form-row",
                                ),
                                css_class="col-12 mb-5",
                            ),
                            Div(
                                Div(
                                    Div(
                                        HTML(
                                            """
                                            <span class="txt-color-gray">International Sizing</span>
                                            """
                                        ),
                                        css_class="col-12 mb-3",
                                    ),
                                    *international_shirt_sizing_field,
                                    HTML(
                                        """
                                        <div class="error_international_shirt_sizing w-100 custom-control custom-checkbox custom-control-inline mt-3" style="display: none">
                                            <input type="checkbox" class="custom-control-input is-invalid">
                                            <p id="" class="invalid-feedback">
                                            <strong>This field is required.</strong></p>
                                        </div>
                                        """
                                    ),
                                    css_class="form-row",
                                ),
                                css_class="col-12 mb-5",
                            ),
                            Div(
                                Div(
                                    Div(
                                        HTML(
                                            """
                                            <span class="txt-color-gray">Select you shirt size</span>
                                            """
                                        ),
                                        css_class="col-12 mb-3",
                                    ),
                                    *shirt_size_field,
                                    HTML(
                                        """
                                        <div class="error_shirt_size w-100 custom-control custom-checkbox custom-control-inline mt-3" style="display: none">
                                            <input type="checkbox" class="custom-control-input is-invalid">
                                            <p id="" class="invalid-feedback">
                                            <strong>This field is required.</strong></p>
                                        </div>
                                        """
                                    ),
                                    css_class="form-row",
                                ),
                                css_class="col-12 mb-5",
                            ),
                            css_class="form-row pl-3 pt-3 border-left-gray-80-1 mx-0",
                        ),
                        css_class="w-100 mb-4",
                    ),
                    Div(
                        HTML(
                            """
                            <span class="fs-18 fw-700 txt-color-white text-uppercase">
                                Shoe Size
                            </span>
                            """
                        ),
                        Div(
                            Div(
                                Div(
                                    HTML(
                                        """
                                        <label for="" class="form-label">Please select your shoe size.</label>
                                        """
                                    ),
                                    css_class="form-group py-0",
                                ),
                                css_class="col-12 mb-3",
                            ),
                            Div(
                                Div(
                                    Div(
                                        HTML(
                                            """
                                            <span class="txt-color-gray">Preferred Sizing</span>
                                            """
                                        ),
                                        css_class="col-12 mb-3",
                                    ),
                                    *shoe_sizing_field,
                                    HTML(
                                        """
                                        <div class="error_shoe_sizing w-100 custom-control custom-checkbox custom-control-inline mt-3" style="display: none">
                                            <input type="checkbox" class="custom-control-input is-invalid">
                                            <p id="" class="invalid-feedback">
                                            <strong>This field is required.</strong></p>
                                        </div>
                                        """
                                    ),
                                    css_class="form-row",
                                ),
                                css_class="col-12 mb-5",
                            ),
                            Div(
                                Div(
                                    Div(
                                        HTML(
                                            """
                                            <span class="txt-color-gray">International Sizing</span>
                                            """
                                        ),
                                        css_class="col-12 mb-3",
                                    ),
                                    *international_shoe_sizing_field,
                                    HTML(
                                        """
                                        <div class="error_international_shoe_sizing w-100 custom-control custom-checkbox custom-control-inline mt-3" style="display: none">
                                            <input type="checkbox" class="custom-control-input is-invalid">
                                            <p id="" class="invalid-feedback">
                                            <strong>This field is required.</strong></p>
                                        </div>
                                        """
                                    ),
                                    css_class="form-row",
                                ),
                                css_class="col-12 mb-4",
                            ),
                            Div(
                                Field("shoe_size", placeholder="Type here"),
                                css_class="col-12 col-md-6 mb-0",
                            ),
                            css_class="form-row pl-3 pt-3 border-left-gray-80-1 mx-0",
                        ),
                        css_class="w-100 mb-4",
                    ),
                    css_class="col-12",
                ),
                Div(FormActions(save_button), css_class="col-md-5 mb-3"),
                skip_button,
                css_class="row",
            ),
        )


class BeveragesAlcoholPreferencesForm(forms.Form):
    milk_selection = forms.MultipleChoiceField(
        label=" ",
        choices=MILK_SELECTIONS,
        widget=forms.widgets.CheckboxSelectMultiple,
    )
    milk_note = forms.CharField(
        widget=forms.Textarea(
            attrs={"rows": 1, "cols": 20, "placeholder": "Type Here"}
        ),
        label="Note to Chef",
        required=False,
    )
    coffee_selection = forms.MultipleChoiceField(
        label=" ",
        choices=COFFEE_SELECTIONS,
        widget=forms.widgets.CheckboxSelectMultiple,
    )
    coffee_note = forms.CharField(
        widget=forms.Textarea(
            attrs={"rows": 1, "cols": 20, "placeholder": "Type Here"}
        ),
        label="Note to Chef",
        required=False,
    )
    tea_selection = forms.MultipleChoiceField(
        label=" ",
        choices=TEA_SELECTIONS,
        widget=forms.widgets.CheckboxSelectMultiple,
    )
    tea_note = forms.CharField(
        widget=forms.Textarea(
            attrs={"rows": 1, "cols": 20, "placeholder": "Type Here"}
        ),
        label="Note to Chef",
        required=False,
    )
    water_selection = forms.MultipleChoiceField(
        label=" ",
        choices=WATER_SELECTIONS,
        widget=forms.widgets.CheckboxSelectMultiple,
    )
    water_note = forms.CharField(
        widget=forms.Textarea(
            attrs={"rows": 1, "cols": 20, "placeholder": "Type Here"}
        ),
        label="Note to Chef",
        required=False,
    )
    juice_selection = forms.MultipleChoiceField(
        label=" ",
        choices=JUICE_SELECTIONS,
        widget=forms.widgets.CheckboxSelectMultiple,
    )
    juice_note = forms.CharField(
        widget=forms.Textarea(
            attrs={"rows": 1, "cols": 20, "placeholder": "Type Here"}
        ),
        label="Note to Chef",
        required=False,
    )
    sodas_and_mixers_selection = forms.MultipleChoiceField(
        label=" ",
        choices=SODAS_MIXERS_SELECTIONS,
        widget=forms.widgets.CheckboxSelectMultiple,
        required=False,
    )
    sodas_and_mixers_note = forms.CharField(
        widget=forms.Textarea(
            attrs={"rows": 1, "cols": 20, "placeholder": "Type Here"}
        ),
        label="Note to Chef",
        required=False,
    )
    add_ons_selection = forms.MultipleChoiceField(
        label=" ",
        choices=ADD_ONS_SELECTIONS,
        widget=forms.widgets.CheckboxSelectMultiple,
    )
    add_ons_note = forms.CharField(
        widget=forms.Textarea(
            attrs={"rows": 1, "cols": 20, "placeholder": "Type Here"}
        ),
        label="Note to Chef",
        required=False,
    )

    def __init__(self, *args, **kwargs):
        view = ""
        alcoholic_preferences = None
        if "view" in kwargs:
            view = kwargs.pop("view")
        if "alcoholic_preferences" in kwargs:
            alcoholic_preferences = kwargs.pop("alcoholic_preferences")
        super().__init__(*args, **kwargs)

        self.helper = FormHelper(self)
        self.helper.form_id = "id-beveragesAlcoholPreferencesForm"
        self.helper.form_class = "form-container-profile ml-0"
        self.helper.form_method = "post"
        self.helper.label_class = "form-label"

        extra_whiskey_html = ""
        extra_brandy_html = ""
        extra_vodka_html = ""
        extra_tequila_html = ""
        extra_rum_html = ""
        extra_liquors_html = ""
        extra_cocktail_html = ""
        extra_port_beer_html = ""
        extra_red_wine_html = ""
        extra_white_wine_html = ""
        extra_rose_wine_html = ""
        extra_champagne_html = ""

        if alcoholic_preferences:
            extra_whiskey_html = generate_html_from_alcohol_dict(
                "whiskey", alcoholic_preferences.extra_whiskey
            )
            extra_brandy_html = generate_html_from_alcohol_dict(
                "brandy", alcoholic_preferences.extra_brandy
            )
            extra_vodka_html = generate_html_from_alcohol_dict(
                "vodka", alcoholic_preferences.extra_vodka
            )
            extra_tequila_html = generate_html_from_alcohol_dict(
                "tequila", alcoholic_preferences.extra_tequila
            )
            extra_rum_html = generate_html_from_alcohol_dict(
                "rum", alcoholic_preferences.extra_rum
            )
            extra_liquors_html = generate_html_from_alcohol_dict(
                "liquors", alcoholic_preferences.extra_liquors
            )
            extra_cocktail_html = generate_html_from_alcohol_dict(
                "cocktail", alcoholic_preferences.extra_cocktail
            )
            extra_port_beer_html = generate_html_from_alcohol_dict(
                "port_beer", alcoholic_preferences.extra_port_beer
            )
            extra_red_wine_html = generate_html_from_alcohol_dict(
                "red_wine", alcoholic_preferences.extra_red_wine
            )
            extra_white_wine_html = generate_html_from_alcohol_dict(
                "white_wine", alcoholic_preferences.extra_white_wine
            )
            extra_rose_wine_html = generate_html_from_alcohol_dict(
                "rose_wine", alcoholic_preferences.extra_rose_wine
            )
            extra_champagne_html = generate_html_from_alcohol_dict(
                "champagne", alcoholic_preferences.extra_champagne
            )

        save_button = Submit(
            "submit",
            "Save",
        )
        ### Form customization for reuseability
        if view == "onboarding":
            save_button = Submit(
                "submit",
                "Save & Continue",
            )
            save_button.id = "submit_button"
            self.form_action = "guests:onboarding_diet_services"

        save_button.field_classes = "btn btn-solid-gold w-100"

        skip_button = None
        if view != "onboarding":
            skip_button = Div(
                Div(
                    HTML(
                        """
                        <a href="{% url 'preferences:food_preferences' %}" class="btn btn-outline-secondary w-100">Skip</a>
                        """
                    ),
                    css_class="form-group",
                ),
                css_class="col-md-5 mb-3",
            )

        milk_selections_field = Div(
            Div(
                HTML(
                    """
                <span class="fs-18 fw-700 txt-color-gold">Milk</span>
                """
                ),
                Div(
                    CustomInlineCheckboxes("milk_selection"),
                    Div(Field("milk_note"), css_class="col-12 mt-3"),
                    css_class="form-row mt-3",
                ),
                css_class="form-group pt-0",
            ),
            css_class="col-12",
        )

        coffee_selections_field = Div(
            Div(
                HTML(
                    """
                <span class="fs-18 fw-700 txt-color-gold">Coffee</span>
                """
                ),
                Div(
                    CustomInlineCheckboxes("coffee_selection"),
                    Div(Field("coffee_note"), css_class="col-12 mt-3"),
                    css_class="form-row mt-3",
                ),
                css_class="form-group pt-0",
            ),
            css_class="col-12",
        )

        tea_selections_field = Div(
            Div(
                HTML(
                    """
                <span class="fs-18 fw-700 txt-color-gold">Tea</span>
                """
                ),
                Div(
                    CustomInlineCheckboxes("tea_selection"),
                    Div(Field("tea_note"), css_class="col-12 mt-3"),
                    css_class="form-row mt-3",
                ),
                css_class="form-group pt-0",
            ),
            css_class="col-12",
        )

        water_selections_field = Div(
            Div(
                HTML(
                    """
                <span class="fs-18 fw-700 txt-color-gold">Water</span>
                """
                ),
                Div(
                    CustomInlineCheckboxes("water_selection"),
                    Div(Field("water_note"), css_class="col-12 mt-3"),
                    css_class="form-row mt-3",
                ),
                css_class="form-group pt-0",
            ),
            css_class="col-12",
        )

        juice_selections_field = Div(
            Div(
                HTML(
                    """
                <span class="fs-18 fw-700 txt-color-gold">Juice</span>
                """
                ),
                Div(
                    CustomInlineCheckboxes("juice_selection"),
                    Div(Field("juice_note"), css_class="col-12 mt-3"),
                    css_class="form-row mt-3",
                ),
                css_class="form-group pt-0",
            ),
            css_class="col-12",
        )

        sodas_mixers_selections_field = Div(
            Div(
                HTML(
                    """
                <span class="fs-18 fw-700 txt-color-gold">Sodas & Mixers</span>
                """
                ),
                Div(
                    CustomInlineCheckboxes("sodas_and_mixers_selection"),
                    Div(Field("sodas_and_mixers_note"), css_class="col-12 mt-3"),
                    css_class="form-row mt-3",
                ),
                css_class="form-group pt-0",
            ),
            css_class="col-12",
        )

        add_ons_selections_field = Div(
            Div(
                HTML(
                    """
                <span class="fs-18 fw-700 txt-color-gold">Add Ons</span>
                """
                ),
                Div(
                    CustomInlineCheckboxes("add_ons_selection"),
                    Div(Field("add_ons_note"), css_class="col-12 mt-3"),
                    css_class="form-row mt-3",
                ),
                css_class="form-group pt-0",
            ),
            css_class="col-12",
        )

        whiskey_name_field = Div(
            HTML(
                """
                <label for="" class="form-label">Whiskey</label>
                <input type="text" class="form-control" name="whiskey_name" id="id_whiskey_name" value="{% if guest.beverages_and_alcoholic_preferences.whiskey_name %}{{ guest.beverages_and_alcoholic_preferences.whiskey_name }}{% else %}{% endif %}" placeholder="Brand, Color, Vineyard / Region">
                """
            ),
            css_class="form-group py-0 w-100",
        )

        whiskey_quantity_field = Div(
            Div(
                HTML(
                    """
                    <button type="button" class="px-0 btn btn-sm bg-transparent d-flex align-items-center" id="minus_bev">
                        <span class="material-icons fs-25 txt-color-gold">remove_circle</span>
                    </button>
                    """
                ),
                css_class="input-group-prepend",
            ),
            HTML(
                """
                <input type="text" class="form-control form-input text-center bg-transparent border-0 p-0" placeholder="0" name="whiskey_quantity" value="{% if guest.beverages_and_alcoholic_preferences.whiskey_quantity %}{{guest.beverages_and_alcoholic_preferences.whiskey_quantity|stringformat:"i"}}{% else %}0{% endif %}" id="ind_bev">
                """
            ),
            Div(
                HTML(
                    """
                    <button type="button" class="px-0 btn btn-sm bg-transparent d-flex align-items-center" id="add_bev">
                        <span class="material-icons fs-25 txt-color-gold">add_circle</span>
                    </button>
                    """
                ),
                css_class="input-group-append",
            ),
            css_class="input-group inc pb-3 px-3",
        )

        brandy_name_field = Div(
            HTML(
                """
                <label for="" class="form-label">Brandy</label>
                <input type="text" class="form-control" name="brandy_name" id="id_brandy_name" value="{% if guest.beverages_and_alcoholic_preferences.brandy_name %}{{ guest.beverages_and_alcoholic_preferences.brandy_name }}{% else %}{% endif %}" placeholder="Brand, Color, Vineyard / Region">
                """
            ),
            css_class="form-group py-0 w-100",
        )

        brandy_quantity_field = Div(
            Div(
                HTML(
                    """
                    <button type="button" class="px-0 btn btn-sm bg-transparent d-flex align-items-center" id="minus_bev">
                        <span class="material-icons fs-25 txt-color-gold">remove_circle</span>
                    </button>
                    """
                ),
                css_class="input-group-prepend",
            ),
            HTML(
                """
                <input type="text" class="form-control form-input text-center bg-transparent border-0 p-0" placeholder="0" name="brandy_quantity" value="{% if guest.beverages_and_alcoholic_preferences.brandy_quantity %}{{ guest.beverages_and_alcoholic_preferences.brandy_quantity|stringformat:"i" }}{% else %}0{% endif %}" id="ind_bev">
                """
            ),
            Div(
                HTML(
                    """
                    <button type="button" class="px-0 btn btn-sm bg-transparent d-flex align-items-center" id="add_bev">
                        <span class="material-icons fs-25 txt-color-gold">add_circle</span>
                    </button>
                    """
                ),
                css_class="input-group-append",
            ),
            css_class="input-group inc pb-3 px-3",
        )

        vodka_name_field = Div(
            HTML(
                """
                <label for="" class="form-label">Vodka</label>
                <input type="text" class="form-control" name="vodka_name" id="id_vodka_name" value="{% if guest.beverages_and_alcoholic_preferences.vodka_name %}{{ guest.beverages_and_alcoholic_preferences.vodka_name }}{% else %}{% endif %}" placeholder="Brand, Color, Vineyard / Region">
                """
            ),
            css_class="form-group py-0 w-100",
        )

        vodka_quantity_field = Div(
            Div(
                HTML(
                    """
                    <button type="button" class="px-0 btn btn-sm bg-transparent d-flex align-items-center" id="minus_bev">
                        <span class="material-icons fs-25 txt-color-gold">remove_circle</span>
                    </button>
                    """
                ),
                css_class="input-group-prepend",
            ),
            HTML(
                """
                <input type="text" class="form-control form-input text-center bg-transparent border-0 p-0" placeholder="0" name="vodka_quantity" value="{% if guest.beverages_and_alcoholic_preferences.vodka_quantity %}{{ guest.beverages_and_alcoholic_preferences.vodka_quantity|stringformat:"i" }}{% else %}0{% endif %}" id="ind_bev">
                """
            ),
            Div(
                HTML(
                    """
                    <button type="button" class="px-0 btn btn-sm bg-transparent d-flex align-items-center" id="add_bev">
                        <span class="material-icons fs-25 txt-color-gold">add_circle</span>
                    </button>
                    """
                ),
                css_class="input-group-append",
            ),
            css_class="input-group inc pb-3 px-3",
        )

        tequila_name_field = Div(
            HTML(
                """
                <label for="" class="form-label">Tequila</label>
                <input type="text" class="form-control" name="tequila_name" id="id_tequila_name" value="{% if guest.beverages_and_alcoholic_preferences.tequila_name %}{{ guest.beverages_and_alcoholic_preferences.tequila_name }}{% else %}{% endif %}" placeholder="Brand, Color, Vineyard / Region">
                """
            ),
            css_class="form-group py-0 w-100",
        )

        tequila_quantity_field = Div(
            Div(
                HTML(
                    """
                    <button type="button" class="px-0 btn btn-sm bg-transparent d-flex align-items-center" id="minus_bev">
                        <span class="material-icons fs-25 txt-color-gold">remove_circle</span>
                    </button>
                    """
                ),
                css_class="input-group-prepend",
            ),
            HTML(
                """
                <input type="text" class="form-control form-input text-center bg-transparent border-0 p-0" placeholder="0" name="tequila_quantity" value="{% if guest.beverages_and_alcoholic_preferences.tequila_quantity %}{{ guest.beverages_and_alcoholic_preferences.tequila_quantity|stringformat:"i" }}{% else %}0{% endif %}" id="ind_bev">
                """
            ),
            Div(
                HTML(
                    """
                    <button type="button" class="px-0 btn btn-sm bg-transparent d-flex align-items-center" id="add_bev">
                        <span class="material-icons fs-25 txt-color-gold">add_circle</span>
                    </button>
                    """
                ),
                css_class="input-group-append",
            ),
            css_class="input-group inc pb-3 px-3",
        )

        rum_name_field = Div(
            HTML(
                """
                <label for="" class="form-label">Rum</label>
                <input type="text" class="form-control" name="rum_name" id="id_rum_name" value="{% if guest.beverages_and_alcoholic_preferences.rum_name %}{{ guest.beverages_and_alcoholic_preferences.rum_name }}{% else %}{% endif %}" placeholder="Brand, Color, Vineyard / Region">
                """
            ),
            css_class="form-group py-0 w-100",
        )

        rum_quantity_field = Div(
            Div(
                HTML(
                    """
                    <button type="button" class="px-0 btn btn-sm bg-transparent d-flex align-items-center" id="minus_bev">
                        <span class="material-icons fs-25 txt-color-gold">remove_circle</span>
                    </button>
                    """
                ),
                css_class="input-group-prepend",
            ),
            HTML(
                """
                <input type="text" class="form-control form-input text-center bg-transparent border-0 p-0" placeholder="0" name="rum_quantity" value="{% if guest.beverages_and_alcoholic_preferences.rum_quantity %}{{ guest.beverages_and_alcoholic_preferences.rum_quantity|stringformat:"i" }}{% else %}0{% endif %}" id="ind_bev">
                """
            ),
            Div(
                HTML(
                    """
                    <button type="button" class="px-0 btn btn-sm bg-transparent d-flex align-items-center" id="add_bev">
                        <span class="material-icons fs-25 txt-color-gold">add_circle</span>
                    </button>
                    """
                ),
                css_class="input-group-append",
            ),
            css_class="input-group inc pb-3 px-3",
        )

        liquors_name_field = Div(
            HTML(
                """
                <label for="" class="form-label">Liqueurs</label>
                <input type="text" class="form-control" name="liquors_name" id="id_liquors_name" value="{% if guest.beverages_and_alcoholic_preferences.liquors_name %}{{ guest.beverages_and_alcoholic_preferences.liquors_name }}{% else %}{% endif %}" placeholder="Brand, Color, Vineyard / Region">
                """
            ),
            css_class="form-group py-0 w-100",
        )

        liquors_quantity_field = Div(
            Div(
                HTML(
                    """
                    <button type="button" class="px-0 btn btn-sm bg-transparent d-flex align-items-center" id="minus_bev">
                        <span class="material-icons fs-25 txt-color-gold">remove_circle</span>
                    </button>
                    """
                ),
                css_class="input-group-prepend",
            ),
            HTML(
                """
                <input type="text" class="form-control form-input text-center bg-transparent border-0 p-0" placeholder="0" name="liquors_quantity" value="{% if guest.beverages_and_alcoholic_preferences.liquors_quantity %}{{ guest.beverages_and_alcoholic_preferences.liquors_quantity|stringformat:"i" }}{% else %}0{% endif %}" id="ind_bev">
                """
            ),
            Div(
                HTML(
                    """
                    <button type="button" class="px-0 btn btn-sm bg-transparent d-flex align-items-center" id="add_bev">
                        <span class="material-icons fs-25 txt-color-gold">add_circle</span>
                    </button>
                    """
                ),
                css_class="input-group-append",
            ),
            css_class="input-group inc pb-3 px-3",
        )

        cocktail_name_field = Div(
            HTML(
                """
                <label for="" class="form-label">Cocktail</label>
                <input type="text" class="form-control" name="cocktail_name" id="id_cocktail_name" value="{% if guest.beverages_and_alcoholic_preferences.cocktail_name %}{{ guest.beverages_and_alcoholic_preferences.cocktail_name }}{% else %}{% endif %}" placeholder="Brand, Color, Vineyard / Region">
                """
            ),
            css_class="form-group py-0 w-100",
        )

        cocktail_quantity_field = Div(
            Div(
                HTML(
                    """
                    <button type="button" class="px-0 btn btn-sm bg-transparent d-flex align-items-center" id="minus_bev">
                        <span class="material-icons fs-25 txt-color-gold">remove_circle</span>
                    </button>
                    """
                ),
                css_class="input-group-prepend",
            ),
            HTML(
                """
                <input type="text" class="form-control form-input text-center bg-transparent border-0 p-0" placeholder="0" name="cocktail_quantity" value="{% if guest.beverages_and_alcoholic_preferences.cocktail_quantity %}{{ guest.beverages_and_alcoholic_preferences.cocktail_quantity|stringformat:"i" }}{% else %}0{% endif %}" id="ind_bev">
                """
            ),
            Div(
                HTML(
                    """
                    <button type="button" class="px-0 btn btn-sm bg-transparent d-flex align-items-center" id="add_bev">
                        <span class="material-icons fs-25 txt-color-gold">add_circle</span>
                    </button>
                    """
                ),
                css_class="input-group-append",
            ),
            css_class="input-group inc pb-3 px-3",
        )

        port_beer_name_field = Div(
            HTML(
                """
                <label for="" class="form-label">Port / Beer</label>
                <input type="text" class="form-control" name="port_beer_name" id="id_port_beer_name" value="{% if guest.beverages_and_alcoholic_preferences.port_beer_name %}{{ guest.beverages_and_alcoholic_preferences.port_beer_name }}{% else %}{% endif %}" placeholder="Brand, Color, Vineyard / Region">
                """
            ),
            css_class="form-group py-0 w-100",
        )

        port_beer_quantity_field = Div(
            Div(
                HTML(
                    """
                    <button type="button" class="px-0 btn btn-sm bg-transparent d-flex align-items-center" id="minus_bev">
                        <span class="material-icons fs-25 txt-color-gold">remove_circle</span>
                    </button>
                    """
                ),
                css_class="input-group-prepend",
            ),
            HTML(
                """
                <input type="text" class="form-control form-input text-center bg-transparent border-0 p-0" placeholder="0" name="port_beer_quantity" value="{% if guest.beverages_and_alcoholic_preferences.port_beer_quantity %}{{ guest.beverages_and_alcoholic_preferences.port_beer_quantity|stringformat:"i" }}{% else %}0{% endif %}" id="ind_bev">
                """
            ),
            Div(
                HTML(
                    """
                    <button type="button" class="px-0 btn btn-sm bg-transparent d-flex align-items-center" id="add_bev">
                        <span class="material-icons fs-25 txt-color-gold">add_circle</span>
                    </button>
                    """
                ),
                css_class="input-group-append",
            ),
            css_class="input-group inc pb-3 px-3",
        )

        red_wine_name_field = Div(
            HTML(
                """
                <label for="" class="form-label">Wine (Red)</label>
                <input type="text" class="form-control" name="red_wine_name" id="id_red_wine_name" value="{% if guest.beverages_and_alcoholic_preferences.red_wine_name %}{{ guest.beverages_and_alcoholic_preferences.red_wine_name }}{% else %}{% endif %}" placeholder="Brand, Color, Vineyard / Region">
                """
            ),
            css_class="form-group py-0 w-100",
        )

        red_wine_quantity_field = Div(
            Div(
                HTML(
                    """
                    <button type="button" class="px-0 btn btn-sm bg-transparent d-flex align-items-center" id="minus_bev">
                        <span class="material-icons fs-25 txt-color-gold">remove_circle</span>
                    </button>
                    """
                ),
                css_class="input-group-prepend",
            ),
            HTML(
                """
                <input type="text" class="form-control form-input text-center bg-transparent border-0 p-0" placeholder="0" name="red_wine_quantity" value="{% if guest.beverages_and_alcoholic_preferences.red_wine_quantity %}{{ guest.beverages_and_alcoholic_preferences.red_wine_quantity|stringformat:"i" }}{% else %}0{% endif %}" id="ind_bev">
                """
            ),
            Div(
                HTML(
                    """
                    <button type="button" class="px-0 btn btn-sm bg-transparent d-flex align-items-center" id="add_bev">
                        <span class="material-icons fs-25 txt-color-gold">add_circle</span>
                    </button>
                    """
                ),
                css_class="input-group-append",
            ),
            css_class="input-group inc pb-3 px-3",
        )

        white_wine_name_field = Div(
            HTML(
                """
                <label for="" class="form-label">Wine (White)</label>
                <input type="text" class="form-control" name="white_wine_name" id="id_white_wine_name" value="{% if guest.beverages_and_alcoholic_preferences.white_wine_name %}{{ guest.beverages_and_alcoholic_preferences.white_wine_name }}{% else %}{% endif %}" placeholder="Brand, Color, Vineyard / Region">
                """
            ),
            css_class="form-group py-0 w-100",
        )

        white_wine_quantity_field = Div(
            Div(
                HTML(
                    """
                    <button type="button" class="px-0 btn btn-sm bg-transparent d-flex align-items-center" id="minus_bev">
                        <span class="material-icons fs-25 txt-color-gold">remove_circle</span>
                    </button>
                    """
                ),
                css_class="input-group-prepend",
            ),
            HTML(
                """
                <input type="text" class="form-control form-input text-center bg-transparent border-0 p-0" placeholder="0" name="white_wine_quantity" value="{% if guest.beverages_and_alcoholic_preferences.white_wine_quantity %}{{ guest.beverages_and_alcoholic_preferences.white_wine_quantity|stringformat:"i" }}{% else %}0{% endif %}" id="ind_bev">
                """
            ),
            Div(
                HTML(
                    """
                    <button type="button" class="px-0 btn btn-sm bg-transparent d-flex align-items-center" id="add_bev">
                        <span class="material-icons fs-25 txt-color-gold">add_circle</span>
                    </button>
                    """
                ),
                css_class="input-group-append",
            ),
            css_class="input-group inc pb-3 px-3",
        )

        rose_wine_name_field = Div(
            HTML(
                """
                <label for="" class="form-label">Wine (Rosé)</label>
                <input type="text" class="form-control" name="rose_wine_name" id="id_rose_wine_name" value="{% if guest.beverages_and_alcoholic_preferences.rose_wine_name %}{{ guest.beverages_and_alcoholic_preferences.rose_wine_name }}{% else %}{% endif %}" placeholder="Brand, Color, Vineyard / Region">
                """
            ),
            css_class="form-group py-0 w-100",
        )

        rose_wine_quantity_field = Div(
            Div(
                HTML(
                    """
                    <button type="button" class="px-0 btn btn-sm bg-transparent d-flex align-items-center" id="minus_bev">
                        <span class="material-icons fs-25 txt-color-gold">remove_circle</span>
                    </button>
                    """
                ),
                css_class="input-group-prepend",
            ),
            HTML(
                """
                <input type="text" class="form-control form-input text-center bg-transparent border-0 p-0" placeholder="0" name="rose_wine_quantity" value="{% if guest.beverages_and_alcoholic_preferences.rose_wine_quantity %}{{ guest.beverages_and_alcoholic_preferences.rose_wine_quantity|stringformat:"i" }}{% else %}0{% endif %}" id="ind_bev">
                """
            ),
            Div(
                HTML(
                    """
                    <button type="button" class="px-0 btn btn-sm bg-transparent d-flex align-items-center" id="add_bev">
                        <span class="material-icons fs-25 txt-color-gold">add_circle</span>
                    </button>
                    """
                ),
                css_class="input-group-append",
            ),
            css_class="input-group inc pb-3 px-3",
        )

        champagne_name_field = Div(
            HTML(
                """
                <label for="" class="form-label">Champagne</label>
                <input type="text" class="form-control" name="champagne_name" id="id_champagne_name" value="{% if guest.beverages_and_alcoholic_preferences.champagne_name %}{{ guest.beverages_and_alcoholic_preferences.champagne_name }}{% else %}{% endif %}" placeholder="Brand, Color, Vineyard / Region">
                """
            ),
            css_class="form-group py-0 w-100",
        )

        champagne_quantity_field = Div(
            Div(
                HTML(
                    """
                    <button type="button" class="px-0 btn btn-sm bg-transparent d-flex align-items-center" id="minus_bev">
                        <span class="material-icons fs-25 txt-color-gold">remove_circle</span>
                    </button>
                    """
                ),
                css_class="input-group-prepend",
            ),
            HTML(
                """
                <input type="text" class="form-control form-input text-center bg-transparent border-0 p-0" placeholder="0" name="champagne_quantity" value="{% if guest.beverages_and_alcoholic_preferences.champagne_quantity %}{{ guest.beverages_and_alcoholic_preferences.champagne_quantity|stringformat:"i" }}{% else %}0{% endif %}" id="ind_bev">
                """
            ),
            Div(
                HTML(
                    """
                    <button type="button" class="px-0 btn btn-sm bg-transparent d-flex align-items-center" id="add_bev">
                        <span class="material-icons fs-25 txt-color-gold">add_circle</span>
                    </button>
                    """
                ),
                css_class="input-group-append",
            ),
            css_class="input-group inc pb-3 px-3",
        )

        other_name_field = Div(
            HTML(
                """
                <label for="" class="form-label">Other</label>
                <input type="text" class="form-control" name="other_name" id="id_other_name" value="{% if guest.beverages_and_alcoholic_preferences.other_name %}{{ guest.beverages_and_alcoholic_preferences.other_name }}{% else %}{% endif %}" placeholder="Please indicate">
                """
            ),
            css_class="form-group py-0 w-100",
        )

        other_quantity_field = Div(
            Div(
                HTML(
                    """
                    <button type="button" class="px-0 btn btn-sm bg-transparent d-flex align-items-center" id="minus_bev">
                        <span class="material-icons fs-25 txt-color-gold">remove_circle</span>
                    </button>
                    """
                ),
                css_class="input-group-prepend",
            ),
            HTML(
                """
                <input type="text" class="form-control form-input text-center bg-transparent border-0 p-0" placeholder="0" name="other_quantity" value="{% if guest.beverages_and_alcoholic_preferences.other_quantity %}{{guest.beverages_and_alcoholic_preferences.other_quantity|stringformat:"i"}}{% else %}0{% endif %}" id="ind_bev">
                """
            ),
            Div(
                HTML(
                    """
                    <button type="button" class="px-0 btn btn-sm bg-transparent d-flex align-items-center" id="add_bev">
                        <span class="material-icons fs-25 txt-color-gold">add_circle</span>
                    </button>
                    """
                ),
                css_class="input-group-append",
            ),
            css_class="input-group inc pb-3 px-3",
        )

        self.helper.layout = Layout(
            Div(
                Div(
                    Div(
                        HTML(
                            """
                            <span class="fs-18 fw-700 txt-color-white text-uppercase">
                                Beverages
                            </span>
                            """
                        ),
                        Div(
                            milk_selections_field,
                            coffee_selections_field,
                            tea_selections_field,
                            water_selections_field,
                            juice_selections_field,
                            sodas_mixers_selections_field,
                            add_ons_selections_field,
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
                                Alcohol
                            </span>
                            """
                        ),
                        Div(
                            Div(
                                HTML(
                                    """
                                <div class="col">
                                    <label for="" class="form-label ml-3 d-table">Brand, Color, Vineyard / Region</label>
                                </div>
                                """
                                ),
                                css_class="form-row mb-3",
                            ),
                            Div(
                                Div(
                                    whiskey_name_field,
                                    whiskey_quantity_field,
                                    css_class="col-12 d-flex align-items-end",
                                    id="whiskey_div",
                                ),
                                css_class="col-12 mb-1 d-flex flex-column",
                            ),
                            HTML(extra_whiskey_html),
                            HTML(
                                f"""<a href="javascript:void(0)" class="ml-3 fs-14 fw-300 txt-color-white mb-4" hx-trigger="click" hx-swap="beforebegin" hx-get={reverse("preferences:add_new_alcohol", args=["whiskey"])}>+ Add another option</a>"""
                            ),
                            Div(
                                Div(
                                    brandy_name_field,
                                    brandy_quantity_field,
                                    css_class="col-12 d-flex align-items-end",
                                    id="brandy_div",
                                ),
                                css_class="col-12 mb-1 d-flex flex-column",
                            ),
                            HTML(extra_brandy_html),
                            HTML(
                                f"""<a href="javascript:void(0)" class="ml-3 mb-4 fs-14 fw-300 txt-color-white" hx-trigger="click" hx-swap="beforebegin" hx-get={reverse("preferences:add_new_alcohol", args=["brandy"])}>+ Add another option</a>"""
                            ),
                            Div(
                                Div(
                                    vodka_name_field,
                                    vodka_quantity_field,
                                    css_class="col-12 d-flex align-items-end",
                                    id="vodka_div",
                                ),
                                css_class="col-12 mb-1 d-flex flex-column",
                            ),
                            HTML(extra_vodka_html),
                            HTML(
                                f"""<a href="javascript:void(0)" class="ml-3 mb-4 fs-14 fw-300 txt-color-white" hx-trigger="click" hx-swap="beforebegin" hx-get={reverse("preferences:add_new_alcohol", args=["vodka"])}>+ Add another option</a>"""
                            ),
                            Div(
                                Div(
                                    tequila_name_field,
                                    tequila_quantity_field,
                                    css_class="col-12 d-flex align-items-end",
                                    id="tequila_div",
                                ),
                                css_class="col-12 mb-1 d-flex flex-column",
                            ),
                            HTML(extra_tequila_html),
                            HTML(
                                f"""<a href="javascript:void(0)" class="ml-3 mb-4 fs-14 fw-300 txt-color-white" hx-trigger="click" hx-swap="beforebegin" hx-get={reverse("preferences:add_new_alcohol", args=["tequila"])}>+ Add another option</a>"""
                            ),
                            Div(
                                Div(
                                    rum_name_field,
                                    rum_quantity_field,
                                    css_class="col-12 d-flex align-items-end",
                                    id="rum_div",
                                ),
                                css_class="col-12 mb-1 d-flex flex-column",
                            ),
                            HTML(extra_rum_html),
                            HTML(
                                f"""<a href="javascript:void(0)" class="ml-3 mb-4 fs-14 fw-300 txt-color-white" hx-trigger="click" hx-swap="beforebegin" hx-get={reverse("preferences:add_new_alcohol", args=["rum"])}>+ Add another option</a>"""
                            ),
                            Div(
                                Div(
                                    liquors_name_field,
                                    liquors_quantity_field,
                                    css_class="col-12 d-flex align-items-end",
                                    id="liquors_div",
                                ),
                                css_class="col-12 mb-1 d-flex flex-column",
                            ),
                            HTML(extra_liquors_html),
                            HTML(
                                f"""<a href="javascript:void(0)" class="ml-3 mb-4 fs-14 fw-300 txt-color-white" hx-trigger="click" hx-swap="beforebegin" hx-get={reverse("preferences:add_new_alcohol", args=["liquors"])}>+ Add another option</a>"""
                            ),
                            Div(
                                Div(
                                    cocktail_name_field,
                                    cocktail_quantity_field,
                                    css_class="col-12 d-flex align-items-end",
                                    id="cocktail_div",
                                ),
                                css_class="col-12 mb-1 d-flex flex-column",
                            ),
                            HTML(extra_cocktail_html),
                            HTML(
                                f"""<a href="javascript:void(0)" class="ml-3 mb-4 fs-14 fw-300 txt-color-white" hx-trigger="click" hx-swap="beforebegin" hx-get={reverse("preferences:add_new_alcohol", args=["cocktail"])}>+ Add another option</a>"""
                            ),
                            Div(
                                Div(
                                    port_beer_name_field,
                                    port_beer_quantity_field,
                                    css_class="col-12 d-flex align-items-end",
                                    id="port_beer_div",
                                ),
                                css_class="col-12 mb-1 d-flex flex-column",
                            ),
                            HTML(extra_port_beer_html),
                            HTML(
                                f"""<a href="javascript:void(0)" class="ml-3 mb-4 fs-14 fw-300 txt-color-white" hx-trigger="click" hx-swap="beforebegin" hx-get={reverse("preferences:add_new_alcohol", args=["port_beer"])}>+ Add another option</a>"""
                            ),
                            Div(
                                Div(
                                    red_wine_name_field,
                                    red_wine_quantity_field,
                                    css_class="col-12 d-flex align-items-end",
                                    id="red_wine_div",
                                ),
                                css_class="col-12 mb-1 d-flex flex-column",
                            ),
                            HTML(extra_red_wine_html),
                            HTML(
                                f"""<a href="javascript:void(0)" class="ml-3 mb-4 fs-14 fw-300 txt-color-white" hx-trigger="click" hx-swap="beforebegin" hx-get={reverse("preferences:add_new_alcohol", args=["red_wine"])}>+ Add another option</a>"""
                            ),
                            Div(
                                Div(
                                    white_wine_name_field,
                                    white_wine_quantity_field,
                                    css_class="col-12 d-flex align-items-end",
                                    id="white_wine_div",
                                ),
                                css_class="col-12 mb-1 d-flex flex-column",
                            ),
                            HTML(extra_white_wine_html),
                            HTML(
                                f"""<a href="javascript:void(0)" class="ml-3 mb-4 fs-14 fw-300 txt-color-white" hx-trigger="click" hx-swap="beforebegin" hx-get={reverse("preferences:add_new_alcohol", args=["white_wine"])}>+ Add another option</a>"""
                            ),
                            Div(
                                Div(
                                    rose_wine_name_field,
                                    rose_wine_quantity_field,
                                    css_class="col-12 d-flex align-items-end",
                                    id="rose_wine_div",
                                ),
                                css_class="col-12 mb-1 d-flex flex-column",
                            ),
                            HTML(extra_rose_wine_html),
                            HTML(
                                f"""<a href="javascript:void(0)" class="ml-3 mb-4 fs-14 fw-300 txt-color-white" hx-trigger="click" hx-swap="beforebegin" hx-get={reverse("preferences:add_new_alcohol", args=["rose_wine"])}>+ Add another option</a>"""
                            ),
                            Div(
                                Div(
                                    champagne_name_field,
                                    champagne_quantity_field,
                                    css_class="col-12 d-flex align-items-end",
                                    id="champagne_div",
                                ),
                                css_class="col-12 mb-1 d-flex flex-column",
                            ),
                            HTML(extra_champagne_html),
                            HTML(
                                f"""<a href="javascript:void(0)" class="ml-3 mb-4 fs-14 fw-300 txt-color-white" hx-trigger="click" hx-swap="beforebegin" hx-get={reverse("preferences:add_new_alcohol", args=["champagne"])}>+ Add another option</a>"""
                            ),
                            Div(
                                Div(
                                    other_name_field,
                                    other_quantity_field,
                                    css_class="col-12 d-flex align-items-end",
                                ),
                                css_class="col-12 mb-4 d-flex flex-column",
                            ),
                            css_class="form-row pl-0 pt-3 border-left-gray-80-1 mx-0",
                        ),
                        css_class="w-100 mb-4",
                    ),
                    css_class="col-12",
                ),
                Div(FormActions(save_button), css_class="col-md-5 mb-3"),
                skip_button,
                css_class="row px-3",
            ),
        )


class ShortJetPreferencesForm(forms.Form):
    dietary_restrictions_notes = forms.CharField(
        widget=forms.Textarea(
            attrs={"rows": 1, "cols": 20, "placeholder": "Type Here"}
        ),
        label="Please note any food preference details here",
        required=False,
    )
    dietary_restrictions_other_notes = forms.CharField(
        widget=forms.Textarea(attrs={"rows": 2, "cols": 20}),
        label="",
        required=False,
    )
    breakfast = forms.MultipleChoiceField(
        label=" ",
        choices=ShortJetPreferenceSheet.BreakfastChoices.choices,
        widget=forms.widgets.CheckboxSelectMultiple,
    )
    breakfast_notes = forms.CharField(
        widget=forms.Textarea(
            attrs={"rows": 1, "cols": 20, "placeholder": "Type Here"}
        ),
        label="Note to Chef",
        required=False,
    )
    lunch = forms.MultipleChoiceField(
        label=" ",
        choices=ShortJetPreferenceSheet.LunchChoices.choices,
        widget=forms.widgets.CheckboxSelectMultiple,
    )
    lunch_notes = forms.CharField(
        widget=forms.Textarea(
            attrs={"rows": 1, "cols": 20, "placeholder": "Type Here"}
        ),
        label="Note to Chef",
        required=False,
    )
    dinner = forms.MultipleChoiceField(
        label=" ",
        choices=ShortJetPreferenceSheet.DinnerChoices.choices,
        widget=forms.widgets.CheckboxSelectMultiple,
    )
    dinner_notes = forms.CharField(
        widget=forms.Textarea(
            attrs={"rows": 1, "cols": 20, "placeholder": "Type Here"}
        ),
        label="Note to Chef",
        required=False,
    )
    kids_meals = forms.MultipleChoiceField(
        label=" ",
        choices=KidsChoices.choices,
        widget=forms.widgets.CheckboxSelectMultiple,
    )
    kids_allergies = forms.CharField(
        widget=forms.Textarea(
            attrs={"rows": 2, "cols": 20, "placeholder": "Type Here"}
        ),
        label="Kids Allergies",
        required=False,
    )
    kids_meals_notes = forms.CharField(
        widget=forms.Textarea(
            attrs={"rows": 1, "cols": 20, "placeholder": "Type Here"}
        ),
        label="Note to Chef",
        required=False,
    )
    favorite_flowers = forms.CharField(
        label="What are your favorite flowers?",
        required=False,
        widget=forms.Textarea(
            attrs={"rows": 1, "cols": 20, "placeholder": "Roses, Lilies, etc.,."}
        ),
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.form_id = "id-shortJetFoodPreferencesForm"
        self.helper.form_class = "form-container-profile ml-0"
        self.helper.form_method = "post"
        self.helper.label_class = "form-label"

        save_button = Submit(
            "submit",
            "Save",
        )
        save_button.field_classes = "btn btn-solid-gold w-100"

        dietary_restrictions_field = []
        dietary_restrictions_other_field = []
        for index, list_item in enumerate(DietaryRestrictionChoices.choices):
            if index % 2 == 0:
                dietary_restrictions_field.append(
                    Div(
                        HTML(
                            '<input type="radio" class="form-radio" name="dietary_restrictions" id="dt-cbx-'
                            + str(index + 1)
                            + '" value="'
                            + list_item[0]
                            + '" {% if "'
                            + list_item[0]
                            + '" in dietary_restrictions %}checked{% endif %}><label for="dt-cbx-'
                            + str(index + 1)
                            + '" class="form-radio-label fw-700" required>'
                            + list_item[1]
                            + "</label>"
                        ),
                        css_class="w-100 mb-3",
                    )
                )
            else:
                dietary_restrictions_other_field.append(
                    Div(
                        HTML(
                            '<input type="radio" class="form-radio" name="dietary_restrictions" id="dt-cbx-'
                            + str(index + 1)
                            + '" value="'
                            + list_item[0]
                            + '" {% if "'
                            + list_item[0]
                            + '" in dietary_restrictions %}checked{% endif %}><label for="dt-cbx-'
                            + str(index + 1)
                            + '" class="form-radio-label fw-700">'
                            + list_item[1]
                            + "</label>"
                        ),
                        css_class="w-100 mb-3",
                    )
                )

        dietary_restrictions_main_field = Div(
            Div(
                *dietary_restrictions_field,
                Field("dietary_restrictions_other_notes", placeholder="Type here"),
                HTML(
                    """
                    <div class="error_dietary_restrictions w-100 custom-control custom-checkbox custom-control-inline mt-3" style="display: none">
                        <input type="checkbox" class="custom-control-input is-invalid">
                        <p id="" class="invalid-feedback">
                        <strong>This field is required.</strong></p>
                    </div>
                    """
                ),
                css_class="col-12 col-sm-6",
            ),
            Div(*dietary_restrictions_other_field, css_class="col-12 col-sm-6"),
            Div(
                Field("dietary_restrictions_notes", placeholder="Type here"),
                css_class="col-12",
            ),
            css_class="form-row mt-4",
        )

        breakfast_fields = Div(
            Div(
                HTML(
                    """
                <label for="" class="form-label">Breakfast</label>
                """
                ),
                Div(
                    CustomInlineCheckboxes("breakfast"),
                    Div(Field("breakfast_notes"), css_class="col-12 mt-3"),
                    css_class="form-row mt-3",
                ),
                css_class="form-group pt-0",
            ),
            css_class="col-12",
        )
        lunch_fields = Div(
            Div(
                HTML(
                    """
                <label for="" class="form-label">Lunch</label>
                """
                ),
                Div(
                    CustomInlineCheckboxes("lunch"),
                    Div(Field("lunch_notes"), css_class="col-12 mt-3"),
                    css_class="form-row mt-3",
                ),
                css_class="form-group pt-0",
            ),
            css_class="col-12",
        )
        dinner_fields = Div(
            Div(
                HTML(
                    """
                <label for="" class="form-label">Dinner</label> <br/>
                <small class="txt-color-white fs-50 fw-700">A delicious hot meal is served for flights taken around dinner time.  Please specify your preference below.</small>
                """
                ),
                Div(
                    CustomInlineCheckboxes("dinner"),
                    Div(Field("dinner_notes"), css_class="col-12 mt-3"),
                    css_class="form-row mt-3",
                ),
                css_class="form-group pt-0",
            ),
            css_class="col-12",
        )
        kids_meals_fields = Div(
            Div(
                HTML(
                    """
                <label for="" class="form-label">Kids Meals</label>
                """
                ),
                Div(
                    CustomInlineCheckboxes("kids_meals"),
                    Div(Field("kids_meals_notes"), css_class="col-12 mt-3"),
                    css_class="form-row mt-3",
                ),
                css_class="form-group pt-0",
            ),
            css_class="col-12",
        )
        kids_allergies_fields = Div(
            Field("kids_allergies"),
            css_class="col-12 mt-3",
        )

        self.helper.layout = Layout(
            Div(
                Div(
                    Div(
                        HTML(
                            """
                            <span class=" fs-18 fw-700 txt-color-white text-uppercase">
                                Meal Options
                            </span>
                            """
                        ),
                    ),
                    Div(
                        Div(
                            HTML(
                                """
                            <span class="fs-10 fw-700 txt-color-secondary text-uppercase">Dietary Restrictions</span>
                            """
                            ),
                            Div(
                                Div(
                                    Div(
                                        Div(
                                            Div(
                                                HTML(
                                                    """
                                                <span class="fs-14 txt-color-gold">Dietary Restrictions</span>
                                                <span class="fs-14 txt-color-gray d-table mt-1">Please indicate if you are....</span>
                                                """
                                                ),
                                                css_class="col-md-6",
                                            ),
                                            css_class="form-row",
                                        ),
                                        dietary_restrictions_main_field,
                                        css_class="form-group py-0",
                                    ),
                                    css_class="col-12",
                                ),
                                css_class="form-row pl-3 pt-3 border-left-gray-80-1 mx-0",
                            ),
                            css_class="w-100 mb-4",
                        ),
                        Div(
                            breakfast_fields,
                            lunch_fields,
                            dinner_fields,
                            kids_allergies_fields,
                            kids_meals_fields,
                            css_class="form-row pl-3 pt-3 border-left-gray-80-1 mx-0",
                        ),
                        css_class="w-100 mb-4",
                    ),
                    Div(
                        Div(
                            HTML(
                                """
                                <span class="fs-18 fw-700 txt-color-white text-uppercase">Room Preference</span>
                                """
                            ),
                            css_class="col-12",
                        ),
                        css_class="form-row mt-5 pt-3",
                    ),
                    Div(
                        Div(
                            Div(
                                Div(
                                    Div(
                                        Div(
                                            Field(
                                                "favorite_flowers",
                                            ),
                                            css_class="col-md-12",
                                        ),
                                        css_class="form-row mb-2",
                                    ),
                                    css_class="form-group pt-0 mb-0",
                                ),
                                css_class="col-12",
                            ),
                            css_class="form-row pl-3 pt-3 border-left-gray-80-1 mx-0",
                        ),
                        css_class="w-100 mb-4",
                    ),
                    css_class="col-12",
                ),
                Div(FormActions(save_button), css_class="col-md-5 mb-3"),
                css_class="row mt-5",
            ),
        )


class LongJetPreferencesForm(forms.Form):
    dietary_restrictions_notes = forms.CharField(
        widget=forms.Textarea(
            attrs={"rows": 1, "cols": 20, "placeholder": "Type Here"}
        ),
        label="Please note any food preference details here",
        required=False,
    )
    dietary_restrictions_other_notes = forms.CharField(
        widget=forms.Textarea(attrs={"rows": 2, "cols": 20}),
        label="",
        required=False,
    )
    breakfast = forms.MultipleChoiceField(
        label=" ",
        choices=LongJetPreferenceSheet.BreakfastChoices.choices,
        widget=forms.widgets.CheckboxSelectMultiple,
        required=False,
    )
    breakfast_notes = forms.CharField(
        widget=forms.Textarea(
            attrs={"rows": 1, "cols": 20, "placeholder": "Type Here"}
        ),
        label="Note to Chef",
        required=False,
    )
    lunch = forms.MultipleChoiceField(
        label=" ",
        choices=LongJetPreferenceSheet.LunchChoices.choices,
        widget=forms.widgets.CheckboxSelectMultiple,
        required=False,
    )
    lunch_notes = forms.CharField(
        widget=forms.Textarea(
            attrs={"rows": 1, "cols": 20, "placeholder": "Type Here"}
        ),
        label="Note to Chef",
        required=False,
    )
    dinner = forms.MultipleChoiceField(
        label=" ",
        choices=LongJetPreferenceSheet.DinnerChoices.choices,
        widget=forms.widgets.CheckboxSelectMultiple,
        required=False,
    )
    dinner_notes = forms.CharField(
        widget=forms.Textarea(
            attrs={"rows": 1, "cols": 20, "placeholder": "Type Here"}
        ),
        label="Note to Chef",
        required=False,
    )
    dinner = forms.MultipleChoiceField(
        label=" ",
        choices=LongJetPreferenceSheet.DinnerChoices.choices,
        widget=forms.widgets.CheckboxSelectMultiple,
        required=False,
    )
    dinner_notes = forms.CharField(
        widget=forms.Textarea(
            attrs={"rows": 1, "cols": 20, "placeholder": "Type Here"}
        ),
        label="Note to Chef",
        required=False,
    )
    dinner = forms.MultipleChoiceField(
        label=" ",
        choices=LongJetPreferenceSheet.DinnerChoices.choices,
        widget=forms.widgets.CheckboxSelectMultiple,
        required=False,
    )
    dinner_notes = forms.CharField(
        widget=forms.Textarea(
            attrs={"rows": 1, "cols": 20, "placeholder": "Type Here"}
        ),
        label="Note to Chef",
        required=False,
    )
    fresh_snacks = forms.MultipleChoiceField(
        label=" ",
        choices=LongJetPreferenceSheet.FreshSnacksChoices.choices,
        widget=forms.widgets.CheckboxSelectMultiple,
        required=False,
    )
    fresh_snacks_notes = forms.CharField(
        widget=forms.Textarea(
            attrs={"rows": 1, "cols": 20, "placeholder": "Type Here"}
        ),
        label="Note to Chef",
        required=False,
    )
    pantry_snacks = forms.MultipleChoiceField(
        label=" ",
        choices=LongJetPreferenceSheet.PantrySnacksChoices.choices,
        widget=forms.widgets.CheckboxSelectMultiple,
        required=False,
    )
    pantry_snacks_notes = forms.CharField(
        widget=forms.Textarea(
            attrs={"rows": 1, "cols": 20, "placeholder": "Type Here"}
        ),
        label="Note to Chef",
        required=False,
    )
    kids_meals = forms.MultipleChoiceField(
        label=" ",
        choices=KidsChoices.choices,
        widget=forms.widgets.CheckboxSelectMultiple,
        required=False,
    )
    kids_allergies = forms.CharField(
        widget=forms.Textarea(
            attrs={"rows": 2, "cols": 20, "placeholder": "Type Here"}
        ),
        label="Kids Allergies",
        required=False,
    )
    kids_meals_notes = forms.CharField(
        widget=forms.Textarea(
            attrs={"rows": 1, "cols": 20, "placeholder": "Type Here"}
        ),
        label="Note to Chef",
        required=False,
    )
    favorite_flowers = forms.CharField(
        label="What are your favorite flowers?",
        required=False,
        widget=forms.Textarea(
            attrs={"rows": 1, "cols": 20, "placeholder": "Roses, Lilies, etc.,."}
        ),
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.form_id = "id-longJetFoodPreferencesForm"
        self.helper.form_class = "form-container-profile ml-0"
        self.helper.form_method = "post"
        self.helper.label_class = "form-label"

        save_button = Submit(
            "submit",
            "Save",
        )
        save_button.field_classes = "btn btn-solid-gold w-100"

        dietary_restrictions_field = []
        dietary_restrictions_other_field = []
        for index, list_item in enumerate(DietaryRestrictionChoices.choices):
            if index % 2 == 0:
                dietary_restrictions_field.append(
                    Div(
                        HTML(
                            '<input type="radio" class="form-radio" name="dietary_restrictions" id="dt-cbx-'
                            + str(index + 1)
                            + '" value="'
                            + list_item[0]
                            + '" {% if "'
                            + list_item[0]
                            + '" in dietary_restrictions %}checked{% endif %}><label for="dt-cbx-'
                            + str(index + 1)
                            + '" class="form-radio-label fw-700" required>'
                            + list_item[1]
                            + "</label>"
                        ),
                        css_class="w-100 mb-3",
                    )
                )
            else:
                dietary_restrictions_other_field.append(
                    Div(
                        HTML(
                            '<input type="radio" class="form-radio" name="dietary_restrictions" id="dt-cbx-'
                            + str(index + 1)
                            + '" value="'
                            + list_item[0]
                            + '" {% if "'
                            + list_item[0]
                            + '" in dietary_restrictions %}checked{% endif %}><label for="dt-cbx-'
                            + str(index + 1)
                            + '" class="form-radio-label fw-700">'
                            + list_item[1]
                            + "</label>"
                        ),
                        css_class="w-100 mb-3",
                    )
                )

        dietary_restrictions_main_field = Div(
            Div(
                *dietary_restrictions_field,
                Field("dietary_restrictions_other_notes", placeholder="Type here"),
                HTML(
                    """
                    <div class="error_dietary_restrictions w-100 custom-control custom-checkbox custom-control-inline mt-3" style="display: none">
                        <input type="checkbox" class="custom-control-input is-invalid">
                        <p id="" class="invalid-feedback">
                        <strong>This field is required.</strong></p>
                    </div>
                    """
                ),
                css_class="col-12 col-sm-6",
            ),
            Div(*dietary_restrictions_other_field, css_class="col-12 col-sm-6"),
            Div(
                Field("dietary_restrictions_notes", placeholder="Type here"),
                css_class="col-12",
            ),
            css_class="form-row mt-4",
        )

        breakfast_fields = Div(
            Div(
                HTML(
                    """
                <label for="" class="form-label">Breakfast</label>
                """
                ),
                Div(
                    CustomInlineCheckboxes("breakfast"),
                    Div(Field("breakfast_notes"), css_class="col-12 mt-3"),
                    css_class="form-row mt-3",
                ),
                css_class="form-group pt-0",
            ),
            css_class="col-12",
        )
        lunch_fields = Div(
            Div(
                HTML(
                    """
                <label for="" class="form-label">Lunch</label>
                """
                ),
                Div(
                    CustomInlineCheckboxes("lunch"),
                    Div(Field("lunch_notes"), css_class="col-12 mt-3"),
                    css_class="form-row mt-3",
                ),
                css_class="form-group pt-0",
            ),
            css_class="col-12",
        )
        dinner_fields = Div(
            Div(
                HTML(
                    """
                <label for="" class="form-label">Dinner</label> <br/>
                <small class="txt-color-white fs-50 fw-700">A delicious hot meal is served for flights taken around dinner time.  Please specify your preference below.</small>
                """
                ),
                Div(
                    CustomInlineCheckboxes("dinner"),
                    Div(Field("dinner_notes"), css_class="col-12 mt-3"),
                    css_class="form-row mt-3",
                ),
                css_class="form-group pt-0",
            ),
            css_class="col-12",
        )
        fresh_snacks_fields = Div(
            Div(
                HTML(
                    """
                    <label for="" class="form-label">Fresh Options</label> <br/>
                """
                ),
                Div(
                    CustomInlineCheckboxes("fresh_snacks"),
                    Div(Field("fresh_snacks_notes"), css_class="col-12 mt-3"),
                    css_class="form-row mt-3",
                ),
                css_class="form-group pt-0",
            ),
            css_class="col-12",
        )
        pantry_snacks_fields = Div(
            Div(
                HTML(
                    """
                    <label for="" class="form-label">Pantry Snacks</label> <br/>
                """
                ),
                Div(
                    CustomInlineCheckboxes("pantry_snacks"),
                    Div(Field("pantry_snacks_notes"), css_class="col-12 mt-3"),
                    css_class="form-row mt-3",
                ),
                css_class="form-group pt-0",
            ),
            css_class="col-12",
        )
        kids_meals_fields = Div(
            Div(
                HTML(
                    """
                <label for="" class="form-label">Kids Meals</label>
                """
                ),
                Div(
                    CustomInlineCheckboxes("kids_meals"),
                    Div(Field("kids_meals_notes"), css_class="col-12 mt-3"),
                    css_class="form-row mt-3",
                ),
                css_class="form-group pt-0",
            ),
            css_class="col-12",
        )
        kids_allergies_fields = Div(
            Field("kids_allergies"),
            css_class="col-12 mt-3",
        )

        self.helper.layout = Layout(
            Div(
                Div(
                    Div(
                        HTML(
                            """
                            <span class=" fw-700 txt-color-gold text-uppercase">
                                Meal Options
                            </span>
                            """
                        ),
                    ),
                    Div(
                        Div(
                            HTML(
                                """
                            <span class="fs-10 fw-700 txt-color-secondary text-uppercase">Dietary Restrictions</span>
                            """
                            ),
                            Div(
                                Div(
                                    Div(
                                        Div(
                                            Div(
                                                HTML(
                                                    """
                                                <span class="fs-14 txt-color-gold">Dietary Restrictions</span>
                                                <span class="fs-14 txt-color-gray d-table mt-1">Please indicate if you are....</span>
                                                """
                                                ),
                                                css_class="col-md-6",
                                            ),
                                            css_class="form-row",
                                        ),
                                        dietary_restrictions_main_field,
                                        css_class="form-group py-0",
                                    ),
                                    css_class="col-12",
                                ),
                                css_class="form-row pl-3 pt-3 border-left-gray-80-1 mx-0",
                            ),
                            css_class="w-100 mb-4",
                        ),
                        Div(
                            breakfast_fields,
                            lunch_fields,
                            dinner_fields,
                            kids_allergies_fields,
                            kids_meals_fields,
                            css_class="form-row pl-3 pt-3 border-left-gray-80-1 mx-0",
                        ),
                        css_class="w-100 mb-4",
                    ),
                    Div(
                        HTML(
                            """
                            <span class=" fw-700 txt-color-gold text-uppercase">
                                Snack Options
                            </span>
                            """
                        ),
                        Div(
                            fresh_snacks_fields,
                            pantry_snacks_fields,
                            css_class="form-row pl-3 pt-3 border-left-gray-80-1 mx-0",
                        ),
                        css_class="w-100 mb-4",
                    ),
                    Div(
                        Div(
                            HTML(
                                """
                                <span class="fs-18 fw-700 txt-color-white text-uppercase">Room Preference</span>
                                """
                            ),
                            css_class="col-12",
                        ),
                        css_class="form-row mt-5 pt-3",
                    ),
                    Div(
                        Div(
                            Div(
                                Div(
                                    Div(
                                        Div(
                                            Field(
                                                "favorite_flowers",
                                            ),
                                            css_class="col-md-12",
                                        ),
                                        css_class="form-row mb-2",
                                    ),
                                    css_class="form-group pt-0 mb-0",
                                ),
                                css_class="col-12",
                            ),
                            css_class="form-row pl-3 pt-3 border-left-gray-80-1 mx-0",
                        ),
                        css_class="w-100 mb-4",
                    ),
                    css_class="col-12",
                ),
                Div(FormActions(save_button), css_class="col-md-5 mb-3"),
                css_class="row mt-5",
            ),
        )
