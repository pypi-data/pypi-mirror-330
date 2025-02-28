#include "asgard.hpp"

using precision = asgard::default_precision;

int main(int argc, char **argv)
{
  // -- set up distribution
  auto const [my_rank, num_ranks] = asgard::initialize_distribution();

  // kill off unused processes
  if (my_rank >= num_ranks)
  {
    asgard::finalize_distribution();
    return 0;
  }

  // -- parse cli
  asgard::prog_opts const options(argc, argv);

  // if there were unknown options, throw an error
  options.throw_if_invalid();

  // main call to asgard, does all the work
  asgard::simulate_builtin<precision>(options);

  asgard::finalize_distribution();

  return 0;
}
