
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

variables i0, i1, i2, i3, o0, o1, o2, o3, a1, a2, a3, c;

# Alf will only come if Betty does

# not i0 
o0 <-> (not i0);

# i0i1 or 
o1 <->  (i0 and (not i1)) or ((not i0) and i1);

# a1 
a1 <-> (i0 and i1);

#o2 

o2 <-> (a1 and (not i2)) or ((not a1) and i2);


#a2

a2 <-> (a1 and i2);


# o3 

o3 <-> (i3 or (not a2)) or ((not i3) and a2);

a3 <-> (c and a2);

c <-> (a3); 
