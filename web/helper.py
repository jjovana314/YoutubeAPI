all_inner_keys = ["kind", "channel_id", "video_id", "total_results", "results_page"]
inner_values_type = [str, str, str, int, int]
zipped_keys_types = list(zip(all_inner_keys, inner_values_type))


def validate_type(value: object, type_: type, min_=None, max_=None) -> None:
    if not isinstance(value, type_):
        raise ValueError(f"{value} must be instance of {type_.__name__}")
    
    # if type_ is str:
    #     if min_ is not None and max_ is not None:
    #         if len(value) < min_:
    #             raise ValueError(f"Length of {value} cannot be less than {min_}")
    #         if len(value) > max_:
    #             raise ValueError(f"Length of {value} cannot be greather than {max_}")

    # if type_ is dict:
    #     keys = value.keys()
    #     for key in keys:
    #         if key not in all_inner_keys:
    #             raise KeyError(f"'{key}' is not valid")
    #     for key, type_inner in zipped_keys_types:
    #         try:
    #             current_value = value[key]
    #         except KeyError:
    #             pass
    #         validate_type(current_value, type_inner)

    # if type_ is int:
    #     if min_ is not None and max_ is not None:
    #         if value < min_:
    #             raise ValueError(f"{value} cannot be less than {min_}")
    #         if value > max_:
    #             raise ValueError(f"{value} cannot be greather than {max_}")
                
