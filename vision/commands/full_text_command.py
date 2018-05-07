import numbers
from constants import GRAND_TOTAL_FIELDS

class FullTextCommand():

    def generate_receipt(self, annotated_image_response):
        full_text_annotation = annotated_image_response.full_text_annotation.text
        # Break apart the receipt into new lines
        lines = full_text_annotation.split('\n')

        total_index = self.search_for_location_of_total(lines)
        total = None

        try:
            if total_index:
                total_amount_guess = lines[total_index + 1]
                import pdb; pdb.set_trace()
                if isinstance(total_amount_guess, numbers.Number):
                    total = total_amount_guess
        except IndexError:
            pass


        import pdb; pdb.set_trace()

    def search_for_location_of_total(self, lines):
        # Look for the word total and if there is a numeric field in the
        # subsequent element
        for index, line  in enumerate(lines):
            if str(line).upper() in (field.upper() for field in GRAND_TOTAL_FIELDS):
                return index

        return None
