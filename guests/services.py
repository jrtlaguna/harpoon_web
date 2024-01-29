from datetime import date
from typing import BinaryIO, Optional

from authentication.models import User
from guests.models import GuestProfile
from charter.models import GuestDetail


def create_guest_account(
    *,
    first_name: str,
    last_name: str,
    email: str,
    phone_number: str,
    password: str,
) -> User:
    """
    Creates an Guest account given the details provided.
    """
    user = User.objects.create(
        first_name=first_name,
        last_name=last_name,
        email=email,
        role=User.Roles.GUEST,
    )
    user.set_password(password)
    user.save()

    GuestProfile.objects.create(user=user, phone_number=phone_number)

    return user


def create_guest_detail(
    *,
    user: User,
    first_name: str,
    last_name: str,
    email: str,
    phone_number: str,
    emergency_contact: str,
    emergency_relation: str,
    emergency_phone: str,
    address_street: str,
    address_number: str,
    address_city: str,
    address_state: str,
    address_zipcode: str,
    address_country: str,
    medical_issues: str,
    nationality: str,
    passport_number: str,
    passport_expiration: date,
    date_of_birth: date,
    allergies: str,
    medications: str,
    salutation_nickname: str,
    high_priority_details: str,
    lactose_intolerant: bool,
    shellfish_allergy: bool,
    nut_allergy: bool,
    gluten_free: bool,
    none_food_sensitivity: bool,
    other: bool,
    other_notes: str,
    passport: Optional[BinaryIO],
) -> GuestDetail:
    try:
        guest_details = GuestDetail.objects.create(
            first_name=first_name,
            last_name=last_name,
            email=email,
            emergency_contact=emergency_contact,
            emergency_relation=emergency_relation,
            emergency_phone=emergency_phone,
            address_street=address_street,
            address_number=address_number,
            address_city=address_city,
            address_state=address_state,
            address_zipcode=address_zipcode,
            address_country=address_country,
            nationality=nationality,
            passport_number=passport_number,
            passport_expiration=passport_expiration,
            date_of_birth=date_of_birth,
            medical_issues=medical_issues,
            allergies=allergies,
            medications=medications,
            lactose_intolerant=lactose_intolerant,
            shellfish_allergy=shellfish_allergy,
            nut_allergy=nut_allergy,
            gluten_free=gluten_free,
            none_food_sensitivity=none_food_sensitivity,
            other=other,
            other_notes=other_notes,
            salutation_nickname=salutation_nickname,
            high_priority_details=high_priority_details,
            profile=user.guest_profile,
            passport=passport,
        )

        user.guest_profile.phone_number = phone_number
        user.email = email
        user.save()
    except Exception as e:
        print(e)

    return guest_details


def update_guest_detail(
    *,
    guest_detail: GuestDetail,
    first_name: str,
    last_name: str,
    email: str,
    phone_number: str,
    emergency_contact: str,
    emergency_relation: str,
    emergency_phone: str,
    address_street: str,
    address_number: str,
    address_city: str,
    address_state: str,
    address_zipcode: str,
    address_country: str,
    nationality: str,
    passport_number: str,
    passport_expiration: date,
    date_of_birth: date,
    medical_issues: str,
    allergies: str,
    medications: str,
    salutation_nickname: str,
    high_priority_details: str,
    lactose_intolerant: bool,
    shellfish_allergy: bool,
    nut_allergy: bool,
    gluten_free: bool,
    none_food_sensitivity: bool,
    other: bool,
    other_notes: str,
    passport: Optional[BinaryIO],
) -> GuestDetail:
    guest_detail.first_name = first_name
    guest_detail.last_name = last_name
    guest_detail.email = email
    guest_detail.emergency_contact = emergency_contact
    guest_detail.emergency_relation = emergency_relation
    guest_detail.emergency_phone = emergency_phone
    guest_detail.address_street = address_street
    guest_detail.address_number = address_number
    guest_detail.address_city = address_city
    guest_detail.address_state = address_state
    guest_detail.address_zipcode = address_zipcode
    guest_detail.address_country = address_country
    guest_detail.medical_issues = medical_issues
    guest_detail.allergies = allergies
    guest_detail.medications = medications
    guest_detail.nationality = nationality
    guest_detail.passport_number = passport_number
    guest_detail.passport_expiration = passport_expiration
    guest_detail.date_of_birth = date_of_birth
    guest_detail.lactose_intolerant = lactose_intolerant
    guest_detail.shellfish_allergy = shellfish_allergy
    guest_detail.nut_allergy = nut_allergy
    guest_detail.gluten_free = gluten_free
    guest_detail.none_food_sensitivity = none_food_sensitivity
    guest_detail.other = other
    guest_detail.other_notes = other_notes
    guest_detail.salutation_nickname = salutation_nickname
    guest_detail.high_priority_details = high_priority_details
    if passport is not None:
        guest_detail.passport.delete()
        guest_detail.passport = passport
    guest_detail.save()

    profile = guest_detail.profile
    profile.phone_number = phone_number
    user = profile.user
    user.first_name = first_name
    user.last_name = last_name
    profile.save()
    user.save()

    return guest_detail


def update_guest_detail_on_register(
    *, user: User, guest_detail: GuestDetail, first_name: str, last_name: str
):
    guest_detail.first_name = first_name
    guest_detail.last_name = last_name
    guest_detail.profile = user.guest_profile
    guest_detail.save()
    return
