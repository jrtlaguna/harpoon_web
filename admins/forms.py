from ast import literal_eval

from crispy_forms.bootstrap import FormActions
from crispy_forms.helper import FormHelper
from crispy_forms.layout import HTML, Div, Field, Layout, Submit
from django import forms
from django.contrib.auth import authenticate
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from django.templatetags.static import static
from django.urls import reverse
from django.utils.safestring import mark_safe

from admins.models import AdminProfile, CrewProfile, GenderChoices
from authentication.models import PasswordResetCode, User


class RegistrationForm(forms.Form):
    first_name = forms.CharField(label="First Name")
    last_name = forms.CharField(label="Last Name")
    role = forms.ChoiceField(choices=AdminProfile.Roles.choices, label="Your Role")
    email = forms.EmailField(label="Email Address")
    phone_number = forms.CharField(max_length=15, label="Phone Number")
    password1 = forms.CharField(
        widget=forms.PasswordInput, label="Password", validators=[validate_password]
    )
    password2 = forms.CharField(widget=forms.PasswordInput, label="Confirm Password")
    accept_toc = forms.BooleanField(
        required=True,
        label=mark_safe(
            "By checking this checkbox you fully understand & agree our "
            "<a href='#' class='txt-color-gold'>Privacy Policy</a>"
            " and "
            "<a href='#' class='txt-color-gold'>Terms and Conditions</a>."
        ),
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.helper = FormHelper(self)
        self.helper.form_id = "id-registrationForm"
        self.helper.form_class = "w-100 m-0 p-0"
        self.helper.form_method = "post"
        self.helper.form_action = "admins:register"
        self.helper.label_class = "form-label"

        self.fields["first_name"].widget.attrs["class"] = "text-only"
        self.fields["last_name"].widget.attrs["class"] = "text-only"
        self.fields["phone_number"].widget.attrs["class"] = "number"
        self.fields["role"].widget.attrs["class"] = "form-select"

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
            "role",
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
                css_class="txt-color-gray",
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
        self.helper.form_action = "admins:forgot_password"
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
            "admins:forgot_password_code", args=[self.email]
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
            f'<a href="{reverse("admins:resend_password_code", args=[self.email])}" class="btn btn-outline-gold mt-3 d-table w-100">Resend Code</a>'
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
            "admins:change_password", args=[self.email, self.code]
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


class SettingsForm(forms.Form):
    admin: User

    first_name = forms.CharField(label="First Name")
    last_name = forms.CharField(label="Last Name")
    role = forms.ChoiceField(choices=AdminProfile.Roles.choices, label="Your Role")
    email = forms.EmailField(label="Email Address")
    phone_number = forms.CharField(max_length=25, label="Phone Number")
    receive_email_notifications = forms.BooleanField(
        required=False,
        label="Receive Email Notifications",
    )

    def __init__(self, *args, **kwargs):
        self.admin = kwargs.pop("admin")
        super().__init__(*args, **kwargs)

        self.helper = FormHelper(self)
        self.helper.form_id = "id-settingsForm"
        self.helper.form_class = ""
        self.helper.form_method = "post"
        self.helper.form_action = reverse("admins:settings")
        self.helper.label_class = "form-label"

        self.fields["role"].widget.attrs["class"] = "form-select"
        self.fields[
            "receive_email_notifications"
        ].label_class = "form-radio-label fw-700 txt-color-white"

        submit_button = Submit(
            "submit",
            "Save",
        )
        submit_button.field_classes = "btn btn-solid-gold w-100"

        separator = HTML(
            f"""
            <div class="separator">
                <div class="line"><hr></div>
                <div><img src="{static('core/img/form-sep-img.svg')}"></div>
                <div class="line"><hr></div>
            </div>
            """
        )

        self.helper.layout = Layout(
            (
                Div(
                    Div(
                        Div(
                            HTML(
                                '<span class="fs-18 fw-700 txt-color-white text-uppercase">Personal Details</span>'
                            ),
                            Div(
                                Div(
                                    Field("first_name"),
                                    css_class="col-12 col-md-6",
                                ),
                                Div(
                                    Field("last_name"),
                                    css_class="col-12 col-md-6",
                                ),
                                Div(
                                    Field("role"),
                                    css_class="col-12 col-md-6",
                                ),
                                HTML(
                                    """
                            <div class="w-100 d-none d-md-block"> </div>
                            """
                                ),
                                Div(
                                    Field(
                                        "phone_number",
                                        id="phone_num",
                                        css_class="form-control w-100 d-table border-0",
                                    ),
                                    css_class="col-12 col-md-6",
                                ),
                                Div(
                                    Field("email", css_class="form-control py-3"),
                                    css_class="col-12 col-md-6",
                                ),
                                css_class="form-row pl-3 pt-3 border-left-gray-80-1 mx-0",
                            ),
                            css_class="w-100",
                        ),
                        css_class="col-12",
                    ),
                    css_class="row",
                )
            ),
            separator,
            Div(
                Div(
                    HTML(
                        """
                    <span class="fs-18 fw-700 txt-color-white text-uppercase">
                        Notifications
                    </span>
                """
                    ),
                    Div(
                        Div(
                            Div(
                                Field("receive_email_notifications"),
                                css_class="col-12",
                            ),
                            css_class="form-row pl-3 pt-3 border-left-gray-80-1 mx-0",
                        ),
                        css_class="w-100 mb-4",
                    ),
                    css_class="col-12",
                ),
                css_class="row",
            ),
            Div(
                FormActions(
                    submit_button,
                    css_class="col-md-6",
                ),
                Div(
                    HTML(
                        f"""
                        <a href="{reverse("admins:settings_change_password")}" class="btn btn-outline-gold d-block">Update Password</a>
                        """
                    ),
                    css_class="col-md-6",
                ),
                css_class="row my-5",
            ),
        )

    def clean_email(self):
        cleaned_email = self.cleaned_data["email"]
        if User.objects.filter(email=cleaned_email).exclude(email=self.admin.email):
            raise ValidationError("Email is already taken.")

        return cleaned_email


class SettingsChangePasswordForm(forms.Form):
    admin: User

    current_password = forms.CharField(
        widget=forms.PasswordInput, label="Current Password"
    )
    password1 = forms.CharField(
        widget=forms.PasswordInput,
        label="Set New Password",
        validators=[validate_password],
    )
    password2 = forms.CharField(widget=forms.PasswordInput, label="Confirm Password")

    def __init__(self, *args, **kwargs):
        self.admin = kwargs.pop("admin")
        super().__init__(*args, **kwargs)

        self.helper = FormHelper(self)
        self.helper.form_id = "id-settingsChangePasswordForm"
        self.helper.form_class = "form-container-profile ml-0"
        self.helper.form_method = "post"
        self.helper.form_action = reverse("admins:settings_change_password")
        self.helper.label_class = "form-label"

        submit_button = Submit(
            "submit",
            "Save",
            css_id="get_started",
        )
        submit_button.field_classes = "btn btn-solid-gold w-100 d-table text-center"

        self.helper.layout = Layout(
            Div(
                Div(
                    Div(
                        HTML(
                            """
            <span class="fs-18 fw-700 txt-color-white text-uppercase">
                Password Details
            </span>
            """
                        ),
                        Div(
                            Div(
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
                            ),
                            Div(
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
                                css_class="col-md-12",
                            ),
                            Div(
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
                                css_class="col-md-12",
                            ),
                            css_class="form-row pl-3 pt-3 border-left-gray-80-1 mx-0",
                        ),
                        css_class="w-100 mb-4",
                    ),
                    css_class="col-12",
                ),
                css_class="row",
            ),
            Div(
                Div(
                    FormActions(
                        submit_button,
                    ),
                    css_class="col-md-6",
                ),
                css_class="row-mb-5",
            ),
        )

    def clean_current_password(self):
        cleaned_current_password = self.cleaned_data["current_password"]
        if not authenticate(email=self.admin.email, password=cleaned_current_password):
            raise ValidationError("Password is incorrect.")

        return cleaned_current_password

    def clean(self):
        cleaned_data = super().clean()
        if not self.errors.get("password1"):
            password1 = cleaned_data.get("password1")
            password2 = cleaned_data.get("password2")

            if password1 != password2:
                raise ValidationError({"password1": ["Passwords do not match."]})


class CrewProfileForm(forms.Form):
    first_name = forms.CharField(label="First Name")
    last_name = forms.CharField(label="Last Name")
    previous_yacht = forms.CharField(label="Previous Yacht", required=False)
    interest = forms.CharField(label="Interest", required=False)
    about = forms.CharField(label="About", required=False)
    crew_type = forms.ChoiceField(
        choices=CrewProfile.CrewTypes.choices, label="Select your User Role"
    )

    def __init__(self, *args, **kwargs):

        if "initial" in kwargs:
            initial: dict = kwargs.pop("initial")
        else:
            initial = None
        super().__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.form_id = "id-crewProfileForm"
        self.helper.form_class = "form-container-profile ml-0"
        self.helper.form_method = "post"
        self.helper.label_class = "form-label"
        self.helper.form_action = reverse("admins:crew_profile_create")
        self.fields["crew_type"].widget.attrs["class"] = "form-select"

        previous_yachts = [
            Div(
                Field("previous_yacht", placeholder="Type Here"),
                css_class="col-12",
            )
        ]

        if initial:
            previous_yachts = []
            self.helper.form_action = reverse(
                "admins:crew_profile_edit", args=[initial.get("id")]
            )
            if initial.get("previous_yacht") not in ["", None]:
                self.fields["first_name"].initial = initial.get("first_name")
                self.fields["last_name"].initial = initial.get("last_name")
                self.fields["crew_type"].initial = initial.get("crew_type")
                self.fields["interest"].initial = initial.get("interest")
                self.fields["about"].initial = initial.get("about")
                if initial.get("previous_yacht").endswith("]"):
                    for yacht in literal_eval(initial.get("previous_yacht")):
                        previous_yachts.append(
                            Div(
                                HTML(
                                    f"""
                            <div class="form-group">
                                <label for="" class="form-label">Previous Yacht</label>
                                <input type="text" name="previous_yacht" class="form-control" value="{yacht}" placeholder="Type here" >
                            </div>
                        """
                                ),
                                css_class="col-12",
                            )
                        )
                else:
                    previous_yachts.append(
                        Div(
                            HTML(
                                f"""
                            <div class="form-group">
                                <label for="" class="form-label">Previous Yacht</label>
                                <input type="text" name="previous_yacht" class="form-control" value="{initial.get("previous_yacht")}" placeholder="Type here" >
                            </div>
                        """
                            ),
                            css_class="col-12",
                        )
                    )

        self.helper.layout = Layout(
            Div(
                Div(
                    Field("first_name", placeholder="Type Here"),
                    css_class="col-12 col-md-6",
                ),
                Div(
                    Field("last_name", placeholder="Type Here"),
                    css_class="col-12 col-md-6",
                ),
                Div(Field("crew_type"), css_class="col-12 col-md-6"),
                *previous_yachts,
                HTML(
                    f"""<a href="#" class="txt-color-gold fw-700 mb-5" hx-trigger="click" hx-swap="beforebegin" hx-get={reverse("admins:add_previous_yacht")}>+ Add Another</a>"""
                ),
                Div(Field("interest", placeholder="Type Here"), css_class="col-12"),
                Div(Field("about", placeholder="Type Here"), css_class="col-12"),
                css_class="form-row pl-3 pt-3 border-left-gray-80-1 mx-0",
            )
        )


class CrewProfileImageForm(forms.Form):
    profile_picture = forms.ImageField()

    def __init__(self, *args, **kwargs):
        crew = kwargs.pop("crew") or None
        super().__init__(*args, **kwargs)

        self.helper = FormHelper(self)
        self.helper.form_id = "id-imageForm"
        self.helper.form_action = reverse(
            "admins:crew_profile_image_upload", args=[crew.id]
        )
        current_image = (
            crew.profile_picture.url
            if crew.profile_picture
            else static("guests/img/account_profile.svg")
        )

        profile_picture_html = HTML(
            f"""
            <div class="row mb-5">
                <div class="col-12 d-flex align-items-center">
                    <div class="profile-thumb-container mr-4">
                        <div class="profile-thumb">
                            <img id="profile_image" src="{current_image}" alt="" class="w-100">
                        </div>

                        <a class="profile-thumb-add sort-link">
                            <label for="profile_picture"><img class="sort-link" src="{static('guests/img/add-icone.svg')}" alt=""></label>
                            <input id="profile_picture" name="profile_picture" type="file" accept=".img, .png, .jpeg, .jpg" hidden />
                        </a>
                    </div>

                    <span class="fs-18 fw-700 txt-color-white">
                        {crew.name if crew else "Crew name"}
                    </span>
                </div>
            </div>
            """
        )

        self.helper.layout = Layout(
            profile_picture_html,
        )


class GuestInfoForm(forms.Form):
    first_name = forms.CharField(label="First Name")
    last_name = forms.CharField(label="Last Name")
    email = forms.EmailField(label="Email")
    gender = forms.ChoiceField(
        choices=GenderChoices.choices, label="Select Gender", required=False
    )
    contact_number = forms.CharField(max_length=15, label="Contact Number")
    nationality = forms.CharField(label="Nationality", required=False)
    notes = forms.CharField(
        widget=forms.Textarea(
            attrs={"rows": 3, "cols": 20, "placeholder": "Type Here"}
        ),
        label="Notes",
        required=False,
    )

    def __init__(self, *args, **kwargs):

        if "initial" in kwargs:
            initial: dict = kwargs.pop("initial")
        else:
            initial = None
        super().__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.form_id = "id-guestInfoForm"
        self.helper.form_class = "form-container-profile ml-0"
        self.helper.form_method = "post"
        self.helper.label_class = "form-label"
        self.fields["gender"].widget.attrs["class"] = "form-select"
        self.fields["first_name"].widget.attrs["class"] = "text-only"
        self.fields["last_name"].widget.attrs["class"] = "text-only"
        self.fields["contact_number"].widget.attrs["class"] = "number"
        self.helper.form_action = reverse("admins:guest_info_create")
        date_of_birth = ""
        if initial:
            self.helper.form_action = reverse(
                "admins:guest_info_edit", args=[initial.get("id")]
            )
            self.fields["first_name"].initial = initial.get("first_name")
            self.fields["last_name"].initial = initial.get("last_name")
            self.fields["email"].initial = initial.get("email")
            self.fields["gender"].initial = initial.get("gender")
            self.fields["contact_number"].initial = initial.get("contact_number")
            date_of_birth = initial.get("date_of_birth")
            self.fields["notes"].initial = initial.get("notes")
            self.fields["nationality"].initial = initial.get("nationality")

        self.helper.layout = Layout(
            Div(
                Div(
                    Field("first_name", placeholder="Type Here"),
                    css_class="col-12 col-md-6",
                ),
                Div(
                    Field("last_name", placeholder="Type Here"),
                    css_class="col-12 col-md-6",
                ),
                Div(
                    Field(
                        "gender",
                        placeholder="Type Here",
                        css_class="form-control col-6",
                    ),
                    css_class="col-12",
                ),
                Div(Field("email", placeholder="Type Here"), css_class="col-6   "),
                Div(
                    Field(
                        "contact_number",
                        placeholder="000 000 000",
                        id="phone_num",
                        css_class="form-control w-100 d-table border-0",
                    ),
                    css_class="col-12 col-md-6",
                ),
                Div(
                    HTML(
                        f"""
                    <label for="" class="form-label">Date of Birth</label>
                    <div class="input-group align-items-center  border-bottom-secondary-1">
                        <input type="text" autocomplete="off" style="height: 3.3em;" class="form-control datepicker border-0" value="{date_of_birth}" name="date_of_birth" placeholder="DD MM YYYY">
                        <div class="input-group-append">
                            <i class="far fa-calendar txt-color-white"></i>
                        </div>
                    </div>"""
                    ),
                    css_class="col-6",
                ),
                Div(
                    Field(
                        "nationality",
                        placeholder="Type Here",
                        css_class="form-control",
                    ),
                    css_class="col-6",
                ),
                Div(Field("notes"), css_class="col-12"),
                css_class="form-row pl-3 pt-3 border-left-gray-80-1 mx-0",
            )
        )


class GuestInfoProfileImageForm(forms.Form):
    profile_picture = forms.ImageField()

    def __init__(self, *args, **kwargs):
        guest_info = kwargs.pop("guest_info") or None
        super().__init__(*args, **kwargs)

        self.helper = FormHelper(self)
        self.helper.form_id = "id-imageForm"
        self.helper.form_action = reverse(
            "admins:guest_info_image_upload", args=[guest_info.id]
        )
        current_image = (
            guest_info.profile_picture.url
            if guest_info.profile_picture
            else static("guests/img/account_profile.svg")
        )

        profile_picture_html = HTML(
            f"""
            <div class="row mb-5">
                <div class="col-12 d-flex align-items-center">
                    <div class="profile-thumb-container mr-4">
                        <div class="profile-thumb">
                            <img id="profile_image" src="{current_image}" alt="" class="w-100">
                        </div>

                        <a class="profile-thumb-add sort-link">
                            <label for="profile_picture"><img class="sort-link" src="{static('guests/img/add-icone.svg')}" alt=""></label>
                            <input id="profile_picture" name="profile_picture" type="file" accept=".img, .png, .jpeg, .jpg" hidden />
                        </a>
                    </div>

                    <span class="fs-18 fw-700 txt-color-white">
                        {guest_info.name if guest_info else "Guest Name"}
                    </span>
                </div>
            </div>
            """
        )

        self.helper.layout = Layout(
            profile_picture_html,
        )
