import os
import csv
import pandas as pd

from django.core.management.base import BaseCommand
from django.conf import settings
from musicworks.models import MusicWork


def get_csv_files():
	"""
	Get the list of CSV files with music works from the 'uploads' directory.
	Exclude files already marked as 'processed'.
	"""
	path = os.path.join(settings.BASE_DIR, settings.UPLOADS_DIR)
	file_list = os.listdir(path)

	return [
		os.path.join(path, filename) for filename in file_list if filename.endswith('.csv')
		and 'processed' not in filename
	]

def mark_file_as_processed(filename):
	"""
	Modify a filename to mark the file as processed and exclude from further processing.
	Might be useful if handling multiple files.
	"""
	path, file = os.path.split(filename)

	return os.path.join(path, f'processed_{file}')


def file_to_db(filename):
	"""
	Read a CSV file with pandas.
	Reconcile music works data with pandas.
	Create DB records with reconciled music works.
	"""
	# Create a Datafrmame from a CSV file, convert 'contributors' to a list.
	df = pd.read_csv(filename, converters={'contributors': lambda x: x.split('|')})
	# Drop music works which cannot be uniquely identified (if necessary).
	df.dropna(thresh=2, inplace=True)
	# Use groupby to reconcile music works with similar iswc or title, incluse all contributors.
	grouped = df.groupby(['title', 'iswc'])
	total = grouped.sum().reset_index()
	# Remove duplicates from the list of contriburors.
	# Sort rows by iswc. Replace NaN with empty strings, if necessary.
	total['contributors'] = total.contributors.map(lambda x: list(set(x)))
	total.sort_values(by=['iswc'], inplace=True)
	total.fillna('', inplace=True)
	
	# Create DB records with reconciled music works.
	MusicWork.objects.bulk_create(
    	MusicWork(**vals) for vals in total.to_dict('records')
	)


class Command(BaseCommand):
	"""
	Process CSV files with music works from the 'uploadas' directory.
	"""

	help = 'Parses the csv file from the directory for musical works and creates DB records'


	def handle(self, *args, **options):
		counter = 0
		for filename in get_csv_files():
			counter += 1
			file_to_db(filename)

			os.rename(filename, mark_file_as_processed(filename))

		self.stdout.write(self.style.SUCCESS(f'{counter} CSV file(s) with music works were processed.'))
