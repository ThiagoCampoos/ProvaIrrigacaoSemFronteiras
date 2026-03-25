import random
from datetime import timedelta
from datetime import timezone as dt_timezone

from django.core.management.base import BaseCommand
from django.db import transaction
from faker import Faker

from people.models import (
    Checkin,
    Checkout,
    HomeServices,
    PatientCompanionCheckin,
    Person,
    ProfessionalServices,
)
from utils.city.all_valid_brasilian_cities_list import cities
from utils.string.format_text import format_text


class Command(BaseCommand):
    help = "Popula o banco com dados de teste consistentes para pessoas, check-ins e servicos."

    def add_arguments(self, parser):
        parser.add_argument("--people", type=int, default=120)
        parser.add_argument("--checkins", type=int, default=90)
        parser.add_argument(
            "--home-services", dest="home_services", type=int, default=75
        )
        parser.add_argument(
            "--professional-services",
            dest="professional_services",
            type=int,
            default=40,
        )
        parser.add_argument(
            "--checkout-rate", dest="checkout_rate", type=float, default=0.35
        )
        parser.add_argument("--seed", type=int, default=42)
        parser.add_argument(
            "--clear",
            action="store_true",
            help="Apaga registros atuais antes de gerar novos dados.",
        )

    def handle(self, *args, **options):
        people_count = max(1, options["people"])
        checkin_count = max(0, options["checkins"])
        home_services_count = max(0, options["home_services"])
        professional_services_count = max(0, options["professional_services"])
        checkout_rate = min(max(options["checkout_rate"], 0.0), 1.0)
        seed = options["seed"]

        random.seed(seed)
        fake = Faker("pt_BR")
        fake.seed_instance(seed)

        with transaction.atomic():
            if options["clear"]:
                self._clear_tables()

            people = self._create_people(fake=fake, amount=people_count)
            checkins = self._create_checkins(
                fake=fake, people=people, amount=checkin_count
            )
            checkouts_count = self._create_checkouts(
                checkins=checkins, checkout_rate=checkout_rate
            )
            home_services = self._create_home_services(
                people=people, amount=home_services_count
            )
            professional_services = self._create_professional_services(
                fake=fake,
                people=people,
                amount=professional_services_count,
            )

        self.stdout.write(self.style.SUCCESS("Seed concluido com sucesso."))
        self.stdout.write(f"- Pessoas: {len(people)}")
        self.stdout.write(f"- Check-ins: {len(checkins)}")
        self.stdout.write(f"- Check-outs: {checkouts_count}")
        self.stdout.write(f"- Servicos domesticos: {home_services}")
        self.stdout.write(f"- Servicos profissionais: {professional_services}")

    def _clear_tables(self):
        Checkout.objects.all().delete()
        PatientCompanionCheckin.objects.all().delete()
        HomeServices.objects.all().delete()
        ProfessionalServices.objects.all().delete()
        Checkin.objects.all().delete()
        Person.objects.all().delete()

    def _create_people(self, fake, amount):
        formatted_cities = [format_text(city) for city in cities]
        states = [state for state, _ in Person.STATE_CHOICES]
        genders = [gender for gender, _ in Person.GENDER_CHOICES]
        residence_types = [residence for residence, _ in Person.RESIDENCE_TYPE_CHOICES]
        ddds = [ddd for ddd, _ in Person.DDD_CHOICES]

        people = []
        used_cpfs = set()
        used_emails = set()

        for _ in range(amount):
            cpf = self._generate_unique_cpf(used_cpfs)
            email = self._generate_unique_email(fake=fake, used_emails=used_emails)
            born_date = fake.date_of_birth(minimum_age=18, maximum_age=90)

            person = Person.objects.create(
                name=fake.name(),
                mother_name=fake.name_female(),
                born_date=born_date,
                email=email,
                gender=random.choice(genders),
                cpf=cpf,
                rg=str(fake.random_number(digits=9, fix_len=True)),
                rg_ssp=random.choice(states),
                state=random.choice(states),
                address_line_1=f"{fake.street_name()}, {fake.building_number()}",
                address_line_2=f"Apto {fake.random_number(digits=3, fix_len=True)}",
                neighbourhood=f"Bairro {fake.first_name()}",
                city=random.choice(formatted_cities),
                postal_code=str(fake.random_number(digits=8, fix_len=True)),
                residence_type=random.choice(residence_types),
                ddd_private_phone=random.choice(ddds),
                private_phone=self._generate_phone(fake=fake),
                ddd_message_phone=random.choice(ddds),
                message_phone=self._generate_phone(fake=fake),
                observation=fake.sentence(nb_words=12),
            )
            people.append(person)

        return people

    def _create_checkins(self, fake, people, amount):
        reasons = [reason for reason, _ in Checkin.REASON_CHOICES]
        checkins = []

        if not people:
            return checkins

        for _ in range(amount):
            person = random.choice(people)
            reason = random.choice(reasons)
            companion = None

            if reason == "patient":
                eligible_companions = [
                    candidate for candidate in people if candidate.id != person.id
                ]
                if eligible_companions:
                    companion = random.choice(eligible_companions)
                else:
                    reason = "professional"

            created_at = fake.date_time_between(
                start_date="-365d", end_date="-1d", tzinfo=dt_timezone.utc
            )

            checkin = Checkin.objects.create(
                person=person,
                reason=reason,
                companion=companion,
                chemotherapy=fake.boolean(chance_of_getting_true=20),
                radiotherapy=fake.boolean(chance_of_getting_true=15),
                surgery=fake.boolean(chance_of_getting_true=10),
                exams=fake.boolean(chance_of_getting_true=35),
                appointment=fake.boolean(chance_of_getting_true=45),
                other=fake.boolean(chance_of_getting_true=10),
                ca_number=str(fake.random_number(digits=8, fix_len=True)),
                social_vacancy=fake.boolean(chance_of_getting_true=30),
                observation=fake.sentence(nb_words=10),
                active=True,
                created_at=created_at,
                updated_at=created_at,
            )

            if reason == "patient" and companion is not None:
                PatientCompanionCheckin.objects.create(
                    patient=person,
                    companion=companion,
                    created_at=created_at,
                    updated_at=created_at,
                )

            checkins.append(checkin)

        return checkins

    def _create_checkouts(self, checkins, checkout_rate):
        if not checkins:
            return 0

        checkout_target = int(round(len(checkins) * checkout_rate))
        checkout_target = min(checkout_target, len(checkins))
        checkout_pool = random.sample(checkins, checkout_target)

        for checkin in checkout_pool:
            checkin.active = False
            checkin.save(update_fields=["active"])

            checkout_created_at = checkin.created_at + timedelta(
                hours=random.randint(2, 72)
            )
            Checkout.objects.create(
                checkin=checkin,
                created_at=checkout_created_at,
                updated_at=checkout_created_at,
            )

        return checkout_target

    def _create_home_services(self, people, amount):
        if not people or amount <= 0:
            return 0

        services_count = min(amount, len(people))
        selected_people = random.sample(people, services_count)

        for person in selected_people:
            values = {
                "breakfast": random.choice([True, False]),
                "lunch": random.choice([True, False]),
                "snack": random.choice([True, False]),
                "dinner": random.choice([True, False]),
                "shower": random.choice([True, False]),
                "sleep": random.choice([True, False]),
            }

            if not any(values.values()):
                values[random.choice(list(values.keys()))] = True

            HomeServices.objects.create(person=person, **values)

        return services_count

    def _create_professional_services(self, fake, people, amount):
        if not people or amount <= 0:
            return 0

        created = 0
        for _ in range(amount):
            ProfessionalServices.objects.create(
                professional=random.choice(people),
                title=fake.sentence(nb_words=4)[:120],
                description=fake.paragraph(nb_sentences=3),
            )
            created += 1

        return created

    def _generate_unique_email(self, fake, used_emails):
        while True:
            email = fake.unique.email()
            if email not in used_emails:
                used_emails.add(email)
                return email

    def _generate_phone(self, fake):
        if fake.boolean(chance_of_getting_true=70):
            return f"9{fake.random_number(digits=8, fix_len=True)}"
        return str(fake.random_number(digits=8, fix_len=True))

    def _generate_unique_cpf(self, used_cpfs):
        while True:
            base = [random.randint(0, 9) for _ in range(9)]
            first_digit = self._calculate_cpf_digit(base, weight_start=10)
            second_digit = self._calculate_cpf_digit(
                base + [first_digit], weight_start=11
            )
            cpf = "".join(str(number) for number in base + [first_digit, second_digit])

            if cpf not in used_cpfs:
                used_cpfs.add(cpf)
                return cpf

    @staticmethod
    def _calculate_cpf_digit(numbers, weight_start):
        total = sum(
            number * weight
            for number, weight in zip(numbers, range(weight_start, 1, -1))
        )
        remainder = (total * 10) % 11
        return 0 if remainder == 10 else remainder
