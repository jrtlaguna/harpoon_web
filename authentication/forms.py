from crispy_forms.bootstrap import FormActions
from crispy_forms.helper import FormHelper
from crispy_forms.layout import HTML, Submit, Layout, Field
from django import forms
from django.contrib.auth.forms import AuthenticationForm


class LoginForm(AuthenticationForm):
    username = forms.EmailField()

    def __init__(self, *args, **kwargs):
        form_action = kwargs.pop("form_action")
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_id = "id-loginForm"
        self.helper.form_class = "w-100 m-0 p-0"
        self.helper.form_method = "post"
        self.helper.form_action = form_action
        self.helper.label_class = "form-label"

        submit_button = Submit(
            "submit",
            "Sign In",
            css_id="get_started",
        )
        submit_button.field_classes = (
            "btn btn-solid-gold w-100 d-table text-center mt-5"
        )

        self.helper.layout = Layout(
            Field(
                "username",
                placeholder="Enter Email",
                css_id="email",
                label_class="form-label",
            ),
            HTML(
                """
                <label for="password" class="form-label">Password</label>
                <div class="input">
                    <input type="password" placeholder="Enter Password" name="password" class="input__password" id="input-pass">
                    <i class='bx bx-hide input__icon' id="input-icon" ></i>
                </div>
                """
            ),
            FormActions(
                submit_button,
            ),
        )
