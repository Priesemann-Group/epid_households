import households as hh

# main run
hh.run_all(0.85, 0.2,  mean='europe_as_country')

# different gamma
hh.run_all(0.7,  0.2,  mean='europe_as_country')
hh.run_all(1.0,  0.2,  mean='europe_as_country')

# different a_h
hh.run_all(0.85, 0.18, mean='europe_as_country')
hh.run_all(0.85, 0.22, mean='europe_as_country')

# different mean
hh.run_all(0.85, 0.2,  mean='basic_mean')
hh.run_all(0.85, 0.2,  mean='weighted_mean')
