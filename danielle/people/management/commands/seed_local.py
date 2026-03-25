from django.core.management import BaseCommand, call_command


class Command(BaseCommand):
    help = (
        "Prepara rapidamente o banco local para testes e demos. "
        "Opcionalmente aplica migracoes e executa seed_db com parametros padrao."
    )

    def add_arguments(self, parser):
        parser.add_argument(
            "--migrate",
            action="store_true",
            help="Executa migracoes antes de popular os dados.",
        )
        parser.add_argument(
            "--no-input",
            action="store_true",
            help="Nao solicita confirmacoes interativas.",
        )
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
            default=True,
            help="Limpa os registros atuais antes de gerar novos dados (padrao: ativo).",
        )
        parser.add_argument(
            "--no-clear",
            dest="clear",
            action="store_false",
            help="Mantem registros atuais e adiciona novos dados.",
        )

    def handle(self, *args, **options):
        if options["migrate"]:
            self.stdout.write(self.style.NOTICE("Aplicando migracoes..."))
            call_command("migrate", interactive=not options["no_input"])

        should_clear = options["clear"]

        self.stdout.write(
            self.style.NOTICE("Executando seed_db para ambiente local...")
        )
        call_command(
            "seed_db",
            people=options["people"],
            checkins=options["checkins"],
            home_services=options["home_services"],
            professional_services=options["professional_services"],
            checkout_rate=options["checkout_rate"],
            seed=options["seed"],
            clear=should_clear,
        )

        strategy = "com limpeza" if should_clear else "sem limpeza"
        self.stdout.write(
            self.style.SUCCESS(f"Ambiente local preparado com sucesso ({strategy}).")
        )
