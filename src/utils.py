def input_error(func):
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except ValueError:
            return "Incorrect value, please try again"
        except IndexError:
            return "Enter user name"  # для phone
        except KeyError as e:
            return f"Contact {e} not found"  # для phone/change

    return inner


def parse_input(user_input):
    cmd, *args = user_input.split()
    cmd = cmd.strip().lower()
    return cmd, *args
