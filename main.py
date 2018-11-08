#!/usr/bin/python3

import argparse
import os
import shutil
import subprocess
import sys


def main():
    parser = argparse.ArgumentParser()
    sp = parser.add_subparsers()

    sp_project = sp.add_parser("project", help="create a new project")
    sp_project.set_defaults(func=create_project)
    sp_project.add_argument("name", type=str, action="store")

    sp_exe = sp.add_parser("exe", help="add an executable to a project")
    sp_exe.set_defaults(func=create_executable)
    sp_exe.add_argument("name", type=str, action="store")

    sp_lib = sp.add_parser("lib", help="add a library to a project")
    sp_lib.set_defaults(func=create_libraray)
    sp_lib.add_argument("name", type=str, action="store")

    sp_class = sp.add_parser("class", help="create a new class")
    sp_class.set_defaults(func=create_class)
    sp_class.add_argument("name", type=str, action="store")
    sp_class.add_argument("-o", "--header-only", action="store_true")

    try:
        args = parser.parse_args()
        args.func(args)
    except AttributeError:
        parser.print_help()
        sys.exit(0)


def create_project(args):
    from_dired_template("project", args.name)


def create_executable(args):
    from_dired_template("exe", args.name)


def create_libraray(args):
    from_dired_template("lib", args.name)


def create_class(args):

    class_path = args.name.split('/')
    class_name = class_path[-1]
    class_path.pop()

    from_class_templates("header.hpp", class_name, class_path, True)
    if not args.header_only:
        from_class_templates("impl.cpp", class_name, class_path, False)


def from_class_templates(template_name: str, class_name: str,
                         class_path: [str], header: bool = False):

    templ_file = os.path.join(get_template_dir("class"), template_name)
    target_file: str = os.path.join(*[os.getcwd()] + class_path + [class_name])

    if header:
        target_file += ".hpp"
    else:
        target_file += ".cpp"

    try:
        shutil.copyfile(templ_file, target_file)
        sed(["-i", f"s/__CLASS_NAME__/{class_name}/g", target_file])
        if header:
            sed(["-i", f"s/__CLASS_DEF__/{class_name.upper()}/g", target_file])

    except Exception as e:
        print(f"Failed to create class {class_name} with exception {e}")
        exit(1)


def sed(args):
    subprocess.call(["sed"] + args)


def from_dired_template(type: str, name: str):

    templ_dir: str = get_template_dir(type)
    target_dir: str = os.path.join(os.getcwd(), name)

    try:
        shutil.copytree(templ_dir, target_dir)
        init_script = os.path.join(target_dir, "init.sh")
        subprocess.call(["bash", init_script, name])
        subprocess.call(["rm", init_script])
        print(f"Created {type} {name}!")

    except Exception as e:
        print(f"Failed to create {type} {name} with exception {e}")
        exit(1)


def get_template_dir(type: str):
    cppcreate_dir = os.path.dirname(os.path.realpath(__file__))
    return os.path.join(*[cppcreate_dir, "templates", type])


if __name__ == "__main__":
    main()
