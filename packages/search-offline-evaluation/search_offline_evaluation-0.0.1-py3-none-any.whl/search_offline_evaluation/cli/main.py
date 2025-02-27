from dotenv import load_dotenv
import typer


from search_offline_evaluation.cli.logs import cli_log_setup
from search_offline_evaluation.cli.labeling import labeling_app
from search_offline_evaluation.cli.data import app as data_app
from search_offline_evaluation.cli.evaluate import evaluate_app

main_app = typer.Typer()
main_app.add_typer(labeling_app, name="labeling")
main_app.add_typer(data_app, name="data")
main_app.add_typer(evaluate_app, name="evaluate")


def main() -> None:
    cli_log_setup()
    load_dotenv()
    main_app()


if __name__ == "__main__":
    main()
