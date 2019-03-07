import random

from django.core.management.base import BaseCommand, CommandError
from comments.models import Candidate, Comment

from faker import Faker
from faker.providers import lorem

class Command(BaseCommand):

    def __init__(self, *args, **kwargs):
        super(BaseCommand, self).__init__(*args, **kwargs)
        self.fake = Faker()
        self.fake.add_provider(lorem)

    def add_arguments(self, parser):
        parser.add_argument('--n', type=lambda x: map(int, x.split(",")), help="Specify the (min, max) number of comments to create for each comment. Usage: --n <min, max>")

    def handle(self, *args, **options):
        min_max = list(options.get("n")) or [10,20]
        for candidate in Candidate.objects.all():
            print("="*30)
            no_tries = random.randint(*min_max)
            print(f"Generating {no_tries} entry(s) for {candidate.name}")
            for _ in range(no_tries):
                comment = Comment.objects.create(author=candidate.creator, candidate=candidate, **self._generate_comment_data())
                print(comment)
            print()

    def _generate_comment_data(self):
        return {
            "title": self.fake.sentence(nb_words=6, variable_nb_words=True, ext_word_list=None),
            "type": random.choice(["NT","BR","EV"]) ,
            "text": self.fake.paragraph(nb_sentences=5, variable_nb_sentences=True, ext_word_list=None),
        }
