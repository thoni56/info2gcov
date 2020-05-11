# info2gcov

Extract coverage data in an info-file created by `lcov` to separate
`.gcov` files, one for each source file.

# Usage

    info2gcov [-q] [-h] <info-file>

`info2gcov` will write `.gcov`-files where the source files are. It will
silently skip any files it cannot write to.

# Rationale

I wanted to use the Emacs `cov-mode` but it only could parse `gcov` files.

My tests produces separate coverage data files because I want to run them in
parallel (see sidebar). `gcov` could not handle this, neither could `gcovr`
for some reason.

Using `lcov` to produce separate `.info` files allowed me to aggregate all
those into a `total.info`.

This script added the final piece, extract aggregated coverage data to
separate `.gcov`-files.

# Sidebar: running tests with coverage in parallel

If you have `--coverage` it is not possible to run tests in parallel because
the writing of coverage data to the `.gcda`-files will clash.

The only solution is to create separate coverage data sets by using the
`GCOV_PREFIX` to set a directory where data will be stored (instead of in the
original object directory).

Then you have to merge all the `.info`-files into one with

    lcov --add-tracefile test1.info <...> -o total.info
