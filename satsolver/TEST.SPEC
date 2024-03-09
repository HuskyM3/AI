
# Organizing a Party
#
# Which combinations of five friends could be invited
# to a party, if there are some constraint that prevent
# inviting them all?

# Declare a propositional variable for each friend.
# Variable X being TRUE means "X is invited" and
# X being FALSE means "X is not invited".
#
# A = Alf
# B = Betty
# C = Cathy
# D = Derek
# E = Ellie

variables A,B,C,D,E;

# Alf will only come if Betty does

not B -> not A;

# Betty and Cathy will argue (Don’t let both in!)

not B | not C;

# Cathy or Derek needed as DJ

C | D;

# Alf is Ellie’s ex: the two only with her hubby Derek

(A and E) -> D;

# Derek can’t stand Betty

not (B and D);

# You could additional constraint to rule out too "small" parties.
