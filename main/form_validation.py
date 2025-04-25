import pickle

def add_form(form_id):
    try:
        with open("form_ids.dat", "ab") as f:
            pickle.dump(form_id, f)
        # print(f"Form ID {form_id} saved successfully.")
    except Exception as e:
        print(f"Error saving form ID: {e}")

def remove_form(form_id):
    try:
        form_ids = []
        with open("form_ids.dat", "rb") as f:
            while True:
                try:
                    saved_form_id = pickle.load(f)
                    form_ids.append(saved_form_id)
                except EOFError:
                    break

        form_ids = [f_id for f_id in form_ids if f_id != form_id]

        # Rewrite the file without the removed ID
        with open("form_ids.dat", "wb") as f:
            for f_id in form_ids:
                pickle.dump(f_id, f)

        # print(f"Form ID {form_id} removed successfully after submission.")
    except Exception as e:
        print(f"Error removing form ID: {e}")

def validate_form(form_id):
    try:
        with open("form_ids.dat", "rb") as f:
            while True:
                try:
                    saved_form_id = pickle.load(f)
                    if saved_form_id == form_id:
                        return True
                except EOFError:
                    break
        return False
    except Exception as e:
        print(f"Error checking form ID: {e}")
        return False

