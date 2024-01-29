from crispy_forms.bootstrap import FormActions, FieldWithButtons, StrictButton
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit, Layout, Field, HTML, Div
from django import forms
from django.contrib.auth import authenticate
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from django.templatetags.static import static
from django.urls import reverse
from django.utils.safestring import mark_safe

from authentication.models import PasswordResetCode
from authentication.models import User


class RegistrationForm(forms.Form):
    first_name = forms.CharField(label="First Name")
    last_name = forms.CharField(label="Last Name")
    email = forms.EmailField(label="Email Address")
    phone_number = forms.CharField(max_length=25, label="Phone Number")
    password1 = forms.CharField(
        widget=forms.PasswordInput, label="Password", validators=[validate_password]
    )
    password2 = forms.CharField(widget=forms.PasswordInput, label="Confirm Password")
    accept_toc = forms.BooleanField(
        required=True,
        label=mark_safe(
            """<span class='small txt-color-gray mt-0'>
                By checking this checkbox you fully understand & agree our
                <a href='#' class='txt-color-gold'>Privacy Policy</a>
                and
                <a href='#' class='txt-color-gold'>Terms and Conditions</a>.
            </span>
            """
        ),
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.helper = FormHelper(self)
        self.helper.form_id = "id-registrationForm"
        self.helper.form_class = "w-100 m-0 p-0"
        self.helper.form_method = "post"
        self.helper.form_action = reverse("guests:register")
        self.helper.label_class = "form-label"

        self.fields["first_name"].widget.attrs["class"] = "text-only"
        self.fields["last_name"].widget.attrs["class"] = "text-only"
        self.fields["phone_number"].widget.attrs["class"] = "number"

        submit_button = Submit(
            "submit",
            "Register",
            css_id="get_started",
        )
        submit_button.field_classes = (
            "btn btn-solid-gold w-100 d-table text-center mt-5"
        )

        self.helper.layout = Layout(
            Field(
                "first_name",
                placeholder="Enter First Name",
            ),
            Field(
                "last_name",
                placeholder="Enter Last Name",
            ),
            Field(
                "email",
                placeholder="Enter Email Address",
            ),
            Field(
                "phone_number",
                placeholder="000 000 000",
                id="phone_num",
            ),
            Div(
                HTML(
                    """
                    <label for="password" class="form-label">Password</label>
                    <div class="input">
                        <input type="password" placeholder="Enter Password" name="password1" class="input__password" id="input-pass1" {% if form.password1.errors %}style="border-color: #dc3545;"{% endif %}>
                        <i class='bx bx-hide input__icon' id="input-icon1" ></i>
                    </div>
                    <span id="error_current_password" class="invalid-feedback"><strong>{{form.password1.errors.as_text|escape}}</strong></span>
                    """
                ),
                css_class="form-group",
            ),
            Div(
                HTML(
                    """
                    <label for="password" class="form-label">Confirm Password</label>
                    <div class="input">
                        <input type="password" placeholder="Confirm Password" name="password2" class="input__password" id="input-pass2" {% if form.password2.errors %}style="border-color: #dc3545;"{% endif %}>
                        <i class='bx bx-hide input__icon' id="input-icon2" ></i>
                    </div>
                    <span id="error_current_password" class="invalid-feedback"><strong>{{form.password2.errors.as_text|escape}}</strong></span>
                    """
                ),
                css_class="form-group",
            ),
            Field(
                "accept_toc",
                css_class="form-checkbox",
            ),
            FormActions(
                submit_button,
            ),
        )

    def clean_email(self):
        email = self.cleaned_data.get("email")
        if User.objects.filter(email=email):
            raise ValidationError("This email already exists.")

        return email

    def clean(self):
        cleaned_data = super().clean()
        if not self.errors.get("password1"):
            password1 = cleaned_data.get("password1")
            password2 = cleaned_data.get("password2")

            if password1 != password2:
                raise ValidationError({"password1": ["Passwords do not match."]})


class ForgotPasswordForm(forms.Form):
    email = forms.EmailField(label="Email Address")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.helper = FormHelper(self)
        self.helper.form_id = "id-forgotPasswordForm"
        self.helper.form_class = "w-100 m-0 p-0"
        self.helper.form_method = "post"
        self.helper.form_action = "guests:forgot_password"
        self.helper.label_class = "form-label"

        submit_button = Submit(
            "submit",
            "Submit",
            css_id="get_started",
        )
        submit_button.field_classes = (
            "btn btn-solid-gold w-100 d-table text-center mt-5"
        )

        self.helper.layout = Layout(
            Field(
                "email",
                placeholder="Enter Email Address",
            ),
            FormActions(
                submit_button,
            ),
        )


class ConfirmForgotPasswordCodeForm(forms.Form):
    char1 = forms.CharField(max_length=1)
    char2 = forms.CharField(max_length=1)
    char3 = forms.CharField(max_length=1)
    char4 = forms.CharField(max_length=1)

    email: str

    def __init__(self, *args, **kwargs):
        self.email = kwargs.pop("email")
        super().__init__(*args, **kwargs)

        self.helper = FormHelper(self)
        self.helper.form_id = "id-forgotPasswordCodeForm"
        self.helper.form_class = "w-100 m-0 p-0 mb-5"
        self.helper.form_method = "post"
        self.helper.form_action = reverse(
            "guests:forgot_password_code", args=[self.email]
        )
        self.helper.label_class = "form-label"

        submit_button = Submit(
            "submit",
            "Submit",
            css_id="get_started",
        )
        submit_button.field_classes = (
            "btn btn-solid-gold w-100 d-table text-center mt-5"
        )

        resend_button = HTML(
            f'<a href="{reverse("guests:resend_password_code", args=[self.email])}" class="btn btn-outline-gold mt-3 d-table w-100">Resend Code</a>'
        )

        self.helper.layout = Layout(
            Div(
                HTML(
                    '<input type="text" class="char_code_verify" id="char1" name="char1" data-next="char2" maxlength="1">'
                ),
                HTML(
                    '<input type="text" class="char_code_verify" id="char2" name="char2" data-next="char3" maxlength="1">'
                ),
                HTML(
                    '<input type="text" class="char_code_verify" id="char3" name="char3" data-next="char4" maxlength="1">'
                ),
                HTML(
                    '<input type="text" class="char_code_verify" id="char4" name="char4" data-next="char5" maxlength="1">'
                ),
                css_class="form-group d-table digit-group",
            ),
            FormActions(
                submit_button,
                resend_button,
                css_class="form-group",
            ),
        )

    def clean(self):
        cleaned_data = super().clean()
        code = f"{cleaned_data['char1']}{cleaned_data['char2']}{cleaned_data['char3']}{cleaned_data['char4']}"
        try:
            password_reset_code = PasswordResetCode.objects.get(
                user__email=self.email,
                code=code,
            )

            if password_reset_code.has_expired:
                raise ValidationError("Code has already expired.")
        except PasswordResetCode.DoesNotExist:
            raise ValidationError("Incorrect code.")


class ChangePasswordForm(forms.Form):
    password = forms.CharField(
        widget=forms.PasswordInput, label="New Password", validators=[validate_password]
    )

    email: str
    code: str

    def __init__(self, *args, **kwargs):
        self.email = kwargs.pop("email")
        self.code = kwargs.pop("code")
        super().__init__(*args, **kwargs)

        self.helper = FormHelper(self)
        self.helper.form_id = "id-changePasswordForm"
        self.helper.form_class = "w-100 m-0 p-0"
        self.helper.form_method = "post"
        self.helper.form_action = reverse(
            "guests:change_password", args=[self.email, self.code]
        )
        self.helper.label_class = "form-label"

        submit_button = Submit(
            "submit",
            "Submit",
            css_id="get_started",
        )
        submit_button.field_classes = "btn btn-solid-gold w-100 d-table text-center"

        self.helper.layout = Layout(
            Div(
                HTML(
                    """
                    <label for="password" class="form-label">Password</label>
                    <div class="input">
                        <input type="password" placeholder="Enter New Password" name="password" class="input__password" id="input-pass" {% if form.password.errors %}style="border-color: #dc3545;"{% endif %}>
                        <i class='bx bx-hide input__icon' id="input-icon" ></i>
                    </div>
                    <span id="error_password" class="invalid-feedback"><strong>{{form.password.errors.as_text|escape}}</strong></span>
                    """
                ),
                css_class="form-group",
            ),
            FormActions(
                submit_button,
            ),
        )

    def clean(self):
        super().clean()
        try:
            password_reset_code = PasswordResetCode.objects.get(
                user__email=self.email,
                code=self.code,
            )

            if password_reset_code.has_expired:
                raise ValidationError("Code has already expired.")

        except PasswordResetCode.DoesNotExist:
            raise ValidationError("Incorrect code.")


class SettingsChangePasswordForm(forms.Form):
    guest: User

    current_password = forms.CharField(
        widget=forms.PasswordInput, label="Current Password"
    )
    password1 = forms.CharField(
        widget=forms.PasswordInput,
        label="Set New Password",
        validators=[validate_password],
    )
    password2 = forms.CharField(widget=forms.PasswordInput, label="Confirm Password")
    email = forms.CharField(widget=forms.EmailInput, label="Email Address")

    def __init__(self, *args, **kwargs):
        self.guest = kwargs.pop("guest")
        super().__init__(*args, **kwargs)

        self.helper = FormHelper(self)
        self.helper.form_id = "id-settingsChangePasswordForm"
        self.helper.form_class = "w-100 m-0 p-0"
        self.helper.form_method = "post"
        self.helper.form_action = reverse("guests:settings_change_password")
        self.helper.label_class = "form-label"

        submit_button = Submit(
            "submit",
            "Save",
            css_id="get_started",
        )
        submit_button.field_classes = "btn btn-solid-gold w-100 d-table text-center"
        email = Div(
            Div(
                HTML(
                    f"""
            <label for="" class="form-label">Email Address</label>
            <input name="email" type="text" placeholder="john.doe@gmail.com" class="form-control" value="{self.guest.email}">
            """
                ),
                css_class="form-group",
            ),
            css_class="col-12",
        )
        email_section = Div(
            Div(
                HTML(
                    '<span class="fs-18 fw-700 txt-color-white text-uppercase">Email</span>'
                ),
                Div(email, css_class="form-row pl-3 pt-3 border-left-gray-80-1 mx-0"),
                css_class="w-100 mb-4",
            ),
            css_class="col-12",
        )
        current_password = Div(
            Div(
                HTML(
                    """
                    <label for="current_password" class="form-label">Current Password</label>
                    <div class="input">
                        <input type="password" placeholder="Enter Current Password" name="current_password" class="input__password" id="id_current_password" {% if form.current_password.errors %}style="border-color: #dc3545;"{% endif %}>
                        <i class='bx bx-hide input__icon' id="input-icon" ></i>
                    </div>
                    <span id="error_current_password" class="invalid-feedback"><strong>{{form.current_password.errors.as_text|escape}}</strong></span>
                    """
                ),
                css_class="form-group",
            ),
            css_class="col-12",
        )
        new_password = Div(
            Div(
                HTML(
                    """
                    <label for="password1" class="form-label">Set New Password</label>
                    <div class="input">
                        <input type="password" placeholder="Enter New Password" name="password1" class="input__password" id="id_password1" {% if form.password1.errors %}style="border-color: #dc3545;"{% endif %}>
                        <i class='bx bx-hide input__icon' id="input-icon1" ></i>
                    </div>
                    <span id="error_current_password" class="invalid-feedback"><strong>{{form.password1.errors.as_text|escape}}</strong></span>
                    """
                ),
                css_class="form-group",
            ),
            css_class="col-12",
        )
        confirm_password = Div(
            Div(
                HTML(
                    """
                    <label for="password2" class="form-label">Confirm New Password</label>
                    <div class="input">
                        <input type="password" placeholder="Confirm New Password" name="password2" class="input__password" id="id_password2">
                        <i class='bx bx-hide input__icon' id="input-icon2" ></i>
                    </div>
                    """
                ),
                css_class="form-group",
            ),
            css_class="col-12",
        )
        self.helper.layout = Layout(
            email_section,
            Div(
                Div(
                    HTML(
                        '<span class="fs-18 fw-700 txt-color-white text-uppercase">Change password</span>'
                    ),
                    Div(
                        current_password,
                        new_password,
                        confirm_password,
                        css_class="form-row pl-3 pt-3 border-left-gray-80-1 mx-0",
                    ),
                    css_class="w-100 mb-4",
                ),
                css_class="col-12",
            ),
            FormActions(
                submit_button,
            ),
        )

    def clean_current_password(self):
        cleaned_current_password = self.cleaned_data["current_password"]
        if not authenticate(email=self.guest.email, password=cleaned_current_password):
            raise ValidationError("Password is incorrect.")

        return cleaned_current_password

    def clean(self):
        cleaned_data = super().clean()
        if not self.errors.get("password1"):
            password1 = cleaned_data.get("password1")
            password2 = cleaned_data.get("password2")

            if password1 != password2:
                raise ValidationError({"password1": ["Passwords do not match."]})


class PrincipleOnboardingForm(forms.Form):
    first_name = forms.CharField(label="First Name")
    last_name = forms.CharField(label="Last Name")
    email = forms.EmailField(label="Email Address")
    phone_number = forms.CharField(max_length=25, label="Phone Number")
    emergency_contact = forms.CharField(
        max_length=25,
        label="Emergency Contact Name:",
    )
    emergency_relation = forms.CharField(
        max_length=25,
        label="Relationship:",
    )
    emergency_phone = forms.CharField(
        max_length=25,
        label="Emergency Contact Phone Number:",
    )
    address_street = forms.CharField(
        max_length=25,
        label="Street Address",
    )
    address_number = forms.CharField(
        max_length=25, label="Suite, Fl. or Apt. #", required=False
    )
    address_city = forms.CharField(
        max_length=25,
        label="City",
    )
    address_state = forms.CharField(
        max_length=25,
        label="State/Province",
    )
    nationality = forms.CharField(
        max_length=75,
        label="Nationality",
    )
    passport_number = forms.CharField(
        max_length=75,
        label="Passport No.",
    )
    passport_expiration = forms.DateField(
        label="Expiration (mm/dd/yyyy)",
        input_formats=["%m/%d/%Y"],
        widget=forms.DateInput(attrs={"autocomplete": "off"}),
    )
    date_of_birth = forms.DateField(
        label="Date of Birth (mm/dd/yyyy)",
        input_formats=["%m/%d/%Y"],
        widget=forms.DateInput(attrs={"autocomplete": "off"}),
    )
    address_zipcode = forms.CharField(
        max_length=25,
        label="Zip code",
    )
    address_country = forms.CharField(
        max_length=25,
        label="Country",
    )
    medical_issues = forms.CharField(
        widget=forms.Textarea(attrs={"rows": 2, "cols": 20}),
        label="Are there any medical issues the crew should know about?",
    )
    allergies = forms.CharField(
        widget=forms.Textarea(attrs={"rows": 2, "cols": 20}),
        label="Do you have any allergies?",
    )
    medications = forms.CharField(
        widget=forms.Textarea(attrs={"rows": 2, "cols": 20}),
        label="Medications",
    )
    salutation_nickname = forms.CharField(
        max_length=25,
        label="How would you like to be addressed?",
    )
    high_priority_details = forms.CharField(
        label="High Priority Details",
        widget=forms.Textarea(
            attrs={
                "placeholder": "Ex. only cotton sheets and blankets, allergic to feathers",
                "rows": 3,
            }
        ),
    )
    lactose_intolerant = forms.BooleanField(
        label="Lactose Intolerant",
        required=False,
    )
    shellfish_allergy = forms.BooleanField(
        label="Shellfish Allergy",
        required=False,
    )
    nut_allergy = forms.BooleanField(
        label="Nut Allergy",
        required=False,
    )
    gluten_free = forms.BooleanField(
        label="Gluten Free",
        required=False,
    )
    none_food_sensitivity = forms.BooleanField(
        label="None",
        required=False,
    )
    other = forms.BooleanField(
        label="Other",
        required=False,
    )
    other_notes = forms.CharField(
        widget=forms.Textarea(attrs={"rows": 3, "cols": 20}),
        label="",
        help_text="",
        required=False,
    )
    passport = forms.FileField(required=False)

    def __init__(self, *args, **kwargs):
        view = kwargs.pop("view")
        user = kwargs.pop("user")
        details = user.guest_profile.details
        super().__init__(*args, **kwargs)

        self.helper = FormHelper(self)
        self.helper.form_id = "id-onboardingForm"
        self.helper.label_class = "form-label"
        self.form_action = "guests:onboarding_profile"
        self.fields["passport"].widget.attrs["hidden"] = "hidden"

        submit_button = Submit(
            "submit",
            "Save & Continue",
            css_id="get_started",
        )
        documents_button = HTML(
            """
            <a href="javascript:void(0)" class="btn btn-solid-gold w-100" data-toggle="modal" data-target="#documents_modal">View Documents</a>.</p>
            """
        )
        if view == "profile_settings":
            submit_button = Submit(
                "submit",
                "Save",
                css_id="get_started",
            )
            self.form_action = "guests:profile"
        submit_button.field_classes = "btn btn-solid-gold w-100"

        first_name = Div(
            Field("first_name", css_class="form-input", placeholder="Type Here"),
            css_class="col-12 col-md-6",
        )
        last_name = Div(
            Field("last_name", css_class="form-input", placeholder="Type Here"),
            css_class="col-12 col-md-6",
        )
        email = Div(
            Field(
                "email",
                css_class="form-input",
                placeholder="example@gmail.com",
            ),
            css_class="col-12",
        )

        phone_number = Div(
            Field(
                "phone_number",
                id="phone_num1",
                placeholder="000 000 000",
                css_class="form-control w-100 d-table border-0",
            ),
            css_class="col-12 col-md-6",
        )
        emergency_contact = Div(
            Field(
                "emergency_contact",
                css_class="form-control",
                placeholder="Type Here",
            ),
            css_class="col-12 col-md-6",
        )
        emergency_relation = Div(
            Field(
                "emergency_relation",
                css_class="form-control",
                placeholder="Type Here",
            ),
            css_class="col-12 col-md-6",
        )
        emergency_phone = HTML(
            f"""
            <div class="col-12 col-md-6">
                <div class="form-group">
                    <label for="" class="form-label">Emergency Contact Phone:</label>
                    <input type="tel" class="form-control w-100 d-table border-0" id="phone_num2" name="emergency_phone" aria-describedby="phone_num2" placeholder="000 000 000" value="{details.emergency_phone if details.emergency_phone else ''}" required>
                </div>
            </div>
            """
        )
        personal_details_div = Div(
            HTML(
                """
                <span class="fs-18 fw-700 txt-color-white text-uppercase">
                    Personal Details
                </span> """
            ),
            Div(
                first_name,
                last_name,
                email,
                phone_number,
                emergency_phone,
                emergency_contact,
                emergency_relation,
                css_class="form-row pl-3 pt-3 border-left-gray-80-1 mx-0",
            ),
            css_class="w-100 mb-4",
        )

        address_street = Div(
            Field("address_street", placeholder="Type Here", css_class="form-control"),
            css_class="col-12 col-md-6",
        )
        address_number = Div(
            Field("address_number", placeholder="Type Here", css_class="form-control"),
            css_class="col-12 col-md-6",
        )
        address_city = Div(
            Field("address_city", placeholder="Type Here", css_class="form-control"),
            css_class="col-12 col-md-6",
        )
        address_state = Div(
            Field("address_state", placeholder="Type Here", css_class="form-control"),
            css_class="col-12 col-md-6",
        )
        address_zipcode = Div(
            Field("address_zipcode", placeholder="Type Here", css_class="form-control"),
            css_class="col-12 col-md-6",
        )
        address_country = Div(
            Field("address_country", placeholder="Type Here", css_class="form-control"),
            css_class="col-12 col-md-6",
        )

        nationality = Div(
            Field("nationality", placeholder="Type Here", css_class="form-control"),
            css_class="col-12 col-md-6",
        )
        passport_number = Div(
            Field("passport_number", placeholder="Type Here", css_class="form-control"),
            css_class="col-12 col-md-6",
        )
        passport_expiration = Div(
            Field(
                "passport_expiration",
                placeholder="mm / dd / yy",
                css_class="form-control",
            ),
            css_class="col-12 col-md-6",
        )
        date_of_birth = Div(
            Field(
                "date_of_birth", placeholder="mm / dd / yy", css_class="form-control"
            ),
            css_class="col-12 col-md-6",
        )

        passport_image = HTML(
            f"""
            <div class="col-12 col-md-6">
                <div class="form-group">
                    <label for="" class="form-label">Upload Passport</label>
                    <input disabled id="passportName" type="text" class="form-control" value="{details.passport.name if details.passport.name else 'No File Selected'}" placeholder="Type here">
                </div>
            </div>
            <div class="col-12 col-md-6 d-flex align-items-center">
                <div class="w-100">
                    <a id="passportButton" href="#" class="btn btn-outline-gold w-100">Browse</a>
                </div>
            </div>
            """
        )
        passport = Field("passport", id="passportFile", hidden="hidden")

        home_address_div = Div(
            HTML(
                '<span class="fs-18 fw-700 txt-color-white text-uppercase">Address</span>'
            ),
            Div(
                address_street,
                address_number,
                address_city,
                address_state,
                address_zipcode,
                address_country,
                css_class="form-row pl-3 pt-3 border-left-gray-80-1 mx-0",
            ),
            css_class="w-100 mb-4",
        )
        if view == "profile_settings":
            passport_div = Div(
                HTML(
                    '<span class="fs-18 fw-700 txt-color-white text-uppercase">Traveler Info</span>'
                ),
                Div(
                    nationality,
                    passport_number,
                    passport_expiration,
                    date_of_birth,
                    passport_image,
                    passport,
                    documents_button,
                    css_class="form-row pl-3 pt-3 border-left-gray-80-1 mx-0",
                ),
                css_class="w-100 mb-4",
            )
        else:
            passport_div = Div(
                HTML(
                    '<span class="fs-18 fw-700 txt-color-white text-uppercase">Traveler Info</span>'
                ),
                Div(
                    nationality,
                    passport_number,
                    passport_expiration,
                    date_of_birth,
                    passport_image,
                    passport,
                    css_class="form-row pl-3 pt-3 border-left-gray-80-1 mx-0",
                ),
                css_class="w-100 mb-4",
            )
        medical_issues = Div(
            Field(
                "medical_issues",
                css_class="form-group",
                placeholder="Type Here",
            ),
            css_class="col-12",
        )
        allergies = Div(
            Field(
                "allergies",
                css_class="form-group",
                placeholder="Type Here",
            ),
            css_class="col-12 col-md-6",
        )
        medications = Div(
            Field(
                "medications",
                css_class="form-group",
                placeholder="Type Here",
            ),
            css_class="col-12 col-md-6",
        )
        health_info_div = Div(
            HTML(
                """<span class="fs-18 fw-700 txt-color-white text-uppercase">Health Info*</span>
                <span class="fs-16 material-icons txt-color-magenta mr-2">
                    flag
                </span>"""
            ),
            Div(
                Div(
                    medical_issues,
                    allergies,
                    medications,
                    Div(
                        Div(
                            HTML(
                                '<label for="" class="form-label">Food Sensitivities</label>'
                            ),
                            Div(
                                HTML(
                                    f"""
                            <div class="col-12 col-sm-6 mb-3">
                                <input type="checkbox" class="form-checkbox" name="lactose_intolerant" {'checked' if details.lactose_intolerant else ''} id="rd-1">
                                <label for="rd-1" class="form-radio-label fw-700">Lactose Intolerant</label>
                            </div>
                            <div class="col-12 col-sm-6 mb-3">
                                <input type="checkbox" class="form-checkbox" name="nut_allergy" {'checked' if details.nut_allergy else ''} id="rd-2">
                                <label for="rd-2" class="form-radio-label fw-700">Nut Allergy</label>
                            </div>
                            <div class="col-12 col-sm-6 mb-3">
                                <input type="checkbox" class="form-checkbox" name="shellfish_allergy" {'checked' if details.shellfish_allergy else ''} id="rd-3">
                                <label for="rd-3" class="form-radio-label fw-700">Shellfish Allergy</label>
                            </div>
                            <div class="col-12 col-sm-6 mb-3">
                                <input type="checkbox" class="form-checkbox" name="gluten_free" {'checked' if details.gluten_free else ''} id="rd-4">
                                <label for="rd-4" class="form-radio-label fw-700">Gluten Free</label>
                            </div>
                            <div class="col-12 col-sm-6 mb-3">
                                <input type="checkbox" class="form-checkbox" name="none_food_sensitivity" {'checked' if details.none_food_sensitivity else ''} id="rd-5">
                                <label for="rd-5" class="form-radio-label fw-700">None</label>
                            </div>
                            <div class="col-12 col-sm-6 mb-3">
                                <input type="checkbox" class="form-checkbox" name="other" {'checked' if details.other else ''} id="rd-6">
                                <label for="rd-6" class="form-radio-label fw-700">Other</label>
                            </div>
                            <div class="col-12 col-sm-6 mb-3">
                            </div>
                            <div class="col-12 col-sm-6 mb-3">
                                <textarea rows="3" cols="20" class="ml-3 py-0 form-control" value="{details.other_notes if details.other_notes else ''}" placeholder="Type here" name="other_notes"></textarea></label>
                            </div>
                                    """
                                ),
                                css_class="form-row mt-3",
                            ),
                            css_class="form-group",
                        ),
                        css_class="col-12",
                    ),
                    css_class="form-row pl-3 pt-3 border-left-gray-80-1 mx-0",
                ),
                css_class="",
            ),
            css_class="w-100 mb-4",
        )
        separator = HTML(
            f"""
            <div class="separator">
                <div class="line"><hr></div>
                <div><img src="{static('core/img/form-sep-img.svg')}"></div>
                <div class="line"><hr></div>
            </div>
            """
        )

        salutation_nickname = Div(
            Field(
                "salutation_nickname",
                css_class="form-group",
                placeholder="Ex. Mrs. , Amy",
            ),
            css_class="col-12",
        )
        high_priority_details = Div(
            Field(
                "high_priority_details",
                css_class="form-group",
                placeholder="Ex. only cotton sheets and blankets, allergic to feathers",
            ),
            css_class="col-12",
        )

        high_priority_info_div = Div(
            HTML(
                """
                <span class="fs-18 fw-700 txt-color-white text-uppercase">HIGH PRIORITY INFO*</span>
                <span class="fs-16 material-icons txt-color-gold mr-2">
                    flag
                </span>
                """
            ),
            Div(
                salutation_nickname,
                high_priority_details,
                css_class="form-row pl-3 pt-3 border-left-gray-80-1 mx-0",
            ),
            css_class="w-100 mb-4",
        )

        self.helper.layout = Layout(
            Div(
                Div(
                    personal_details_div,
                    css_class="col-12",
                ),
                Div(
                    separator,
                    css_class="col-12",
                ),
                Div(
                    home_address_div,
                    css_class="col-12",
                ),
                Div(
                    separator,
                    css_class="col-12",
                ),
                Div(
                    passport_div,
                    css_class="col-12",
                ),
                Div(
                    separator,
                    css_class="col-12",
                ),
                Div(
                    health_info_div,
                    css_class="col-12",
                ),
                Div(
                    separator,
                    css_class="col-12",
                ),
                Div(
                    high_priority_info_div,
                    css_class="col-12",
                ),
                Div(
                    Div(
                        Div(submit_button, css_class="col-md-12"),
                        css_class="row",
                    ),
                    css_class="col-12 mb-3",
                ),
                css_class="row mt-5",
            )
        )


class ProfileImageForm(forms.Form):
    profile_picture = forms.ImageField()

    def __init__(self, *args, **kwargs):
        user = kwargs.pop("user") or None
        super().__init__(*args, **kwargs)

        self.helper = FormHelper(self)
        self.helper.form_id = "id-imageForm"
        self.helper.form_action = "guests:profile_image_upload"
        current_image = (
            user.profile_picture.url
            if user.profile_picture
            else static("guests/img/account_profile.svg")
        )
        profile_picture_html = HTML(
            f"""
            <div class="profile-thumb-container mr-4">
                <div class="profile-thumb">
                    <img id="profile_image" src="{current_image}" alt="" class="w-100">
                </div>
                <a class="profile-thumb-add sort-link">
                    <label for="profile_picture"><img class="sort-link" src="{static('guests/img/add-icone.svg')}" alt=""></label>
                    <input id="profile_picture" name="profile_picture" type="file" accept=".img, .png, .jpeg, .jpg" hidden />
                </a>
            </div>
            """
        )

        self.helper.layout = Layout(
            profile_picture_html,
        )


class DocumentForm(forms.Form):
    document = forms.FileField(
        label="+ Add Documents",
        widget=forms.ClearableFileInput(attrs={"multiple": True}),
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.form_id = "id-fileForm"
        self.helper.form_action = "guests:document_upload"
        upload_button = HTML(
            """
                <div class="col-12 d-flex align-items-center">
                <div class="w-100">
                    <a id="documentButton" href="#" class="btn btn-outline-gold w-100">Upload Additional Documents</a>
                </div>
            </div>
            """
        )
        document = Field("document", id="documentFile", hidden="hidden")

        self.helper.layout = Layout(upload_button, document)
