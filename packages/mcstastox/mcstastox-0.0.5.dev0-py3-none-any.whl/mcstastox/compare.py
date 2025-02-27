import numpy as np
from colorama import Fore, Style
from collections.abc import Sequence
from scipy.spatial.transform import Rotation

from .LoadFile import Data


def is_indexable_sequence(obj):
    return isinstance(obj, (Sequence, np.ndarray)) and not isinstance(obj, (str, bytes))


def compare_values(name, val1, val2):
    """Compare two values and return a formatted string of differences."""
    if val1 == val2:
        return ""

    if isinstance(val1, (int, float)) and isinstance(val2, (int, float)):
        rel_diff = abs(val1 - val2) / max(abs(val1), abs(val2)) * 100 if max(abs(val1), abs(val2)) != 0 else 0
        return f"  {name}: {val1} vs {val2} (Difference: {rel_diff:.2f}%)"

    return f"  {name}: {val1} vs {val2}"


def compare_lists(name, list1, list2):
    """Compare two lists element-wise."""
    output = []
    for i, (v1, v2) in enumerate(zip(list1, list2)):
        diff = compare_values(f"{name}[{i}]", v1, v2)
        if diff:
            output.append(diff)
    return output


def smallest_rotation(R1, R2):
    """
    Compute the smallest rotation needed to go from R1 to R2.

    Parameters:
    R1, R2 : numpy.ndarray
        3x3 rotation matrices.

    Returns:
    axis : numpy.ndarray
        The unit vector representing the axis of rotation.
    angle : float
        The minimal rotation angle in radians.
    """
    # Compute the relative rotation matrix
    R_rel = R2 @ R1.T

    # Convert to axis-angle representation
    rotation = Rotation.from_matrix(R_rel)
    axis_angle = rotation.as_rotvec()

    # Extract rotation axis and angle
    angle = np.linalg.norm(axis_angle)
    axis = axis_angle / angle if angle > 1e-8 else np.array([0, 0, 0])  # Avoid division by zero

    return axis, angle


def dict_element_compare(key, dict1, dict2):
    if key in dict1 and key in dict2:
        # Could be a list type, check
        if is_indexable_sequence(dict1[key]):
            # Could be a matrix type, check
            if is_indexable_sequence(dict1[key][0]):
                # Matrix, do compare for each line
                output = []
                for index, included_list_1 in enumerate(dict1[key]):
                    included_list_2 = dict2[key][index]
                    output.extend(compare_lists(key + "_" + str(index), included_list_1, included_list_2))

                output = [diff for diff in output if diff]  # Remove empty entries

                if len(output) == 0:
                    return ""
                else:
                    if dict1[key].shape == (3,3) and dict2[key].shape == (3,3):
                        axis, angle = smallest_rotation(dict1[key], dict2[key])
                        angle *= 180/np.pi
                        return [f"Rotation matrix differs: {round(angle, 4)} [deg] around {axis}\n{dict1[key]}\n vs \n{dict2[key]}"]
                    else:
                        return [f"Matrix differs: \n{dict1[key]}\n vs \n{dict2[key]}\n"]
            else:
                # Just a list, a do list compare
                return compare_lists(key, dict1[key], dict2[key])
        else:
            return [compare_values(key, dict1[key], dict2[key])]

    elif key not in dict1 and key not in dict2:
        return [""]

    else:
        return [f"didnt both have key {key}"]


def make_model_dict(data_object):

    component_names = data_object.get_components()

    model_dict = {}
    for name in component_names:
        model_dict[name] = {}

        position, rotation = data_object.get_component_placement(name)
        model_dict[name]["global_AT"] = position
        model_dict[name]["global_ROTATION"] = rotation

        # Not all components have parameters, notably arms
        try:
            model_dict[name]["parameters"] = data_object.file_object.get_component_parameters(name)
        except:
            pass

    return model_dict

def compare_model_runs(file1, file2):
    """
    This function compares the instrument models used to make two files

    This includes positions and parameters of components, and is thus dependent
    on the used instrument parameters

    :param file1: McStas generated NeXus file
    :param file2: McStas generated NeXus file
    :return:
    """
    output = []

    with Data(file1) as data1:
        with Data(file2) as data2:

            model_1 = make_model_dict(data1)
            model_2 = make_model_dict(data2)

            all_names = set(model_1.keys()).union(set(model_2.keys()))

            for name in reversed(sorted(all_names)):

                if name in model_1 and name in model_2:
                    component1 = model_1[name]
                    component2 = model_2[name]

                    differences = []

                    # Compare fixed parts
                    differences.extend(dict_element_compare("global_AT", component1, component2))
                    differences.extend(dict_element_compare("global_ROTATION", component1, component2))

                    # Compare parameter-based attributes
                    if "parameters" in component1 and "parameters" in component2:

                        par1 = component1["parameters"]
                        par2 = component2["parameters"]

                        all_par_names = set(par1.keys()).union(set(par2.keys()))

                        for param in all_par_names:
                            val1 = par1.get(param, "(missing)").get("value", "(no value)")
                            val2 = par2.get(param, "(missing)").get("value", "(no value)")
                            differences.append(compare_values(param, val1, val2))

                    differences = [diff for diff in differences if diff]  # Remove empty entries

                    if not differences:
                        output.append(f"{Fore.GREEN}{name} (Identical){Style.RESET_ALL}")
                    else:
                        output.append(f"{Fore.YELLOW}{name} (Differences found){Style.RESET_ALL}")
                        output.extend(differences)

                elif name in model_1 and name not in model_2:
                    output.append(f"component {Fore.RED}{name} (Only in 1){Style.RESET_ALL}")

                elif name not in model_1 and name in model_2:
                    output.append(f"component {Fore.RED}{name} (Only in 2){Style.RESET_ALL}")

    return "\n".join(output)