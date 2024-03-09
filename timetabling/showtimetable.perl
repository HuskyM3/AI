#!/usr/bin/env perl
# 2024 (C) Aalto University, Jussi Rintanen

while(<STDIN>) {
	if( /\bClassTime_([A-Z][a-zA-Z0-9]*)_([A-Z][a-zA-Z0-9]*)_([0-9]+) := 1/i ) {
	    $classtime{"$1-$2-$3"} = 1;
	}

	if( /\bClassTeacher_([A-Z][a-zA-Z0-9]*)_([a-z][a-zA-Z0-9]*)_([a-z][a-zA-Z0-9]*) := 1/i ) {
	    $classteacher{"$1-$2-$3"} = 1;
	}

	if( /\bClassDay_([A-Z][a-zA-Z0-9]*)_([a-z][a-zA-Z0-9]*)_([a-z]+) := 1/i ) {
	    $classday{"$1-$2-$3"} = 1;
	}

}

# Show schedule

@days = ("monday","tuesday","wednesday");
@hours = (8, 9, 10, 11, 12, 13, 14);
@teachers = ("matti","maija","paavo","ritva");
@groups = ("grpA","grpB","grpC");
@classes = ("math1","math2","physics1","physics2","chemistry","english1","english2","history","biology","sports1","sports2","swedish1","swedish2");

# Show the schedule for each group

foreach my $group (@groups) {
    printf("\nSchedule for group %s\n\n",$group);
    printf("    %-25s %-25s %-25s\n","Monday","Tuesday","Wednesday");
    foreach my $hour (@hours) {
	printf("%2d: ",$hour);
	foreach my $day (@days) {
	    $s = "";
	    foreach my $class (@classes) {
		if((%classtime{"$class-$group-$hour"} == 1) && (%classday{"$class-$group-$day"} == 1)) {
		    $s = "$s$class ";
		}
	    }
	    printf("%-24s ",$s);
	}
	printf("\n");
    }
    printf("\n");
}

# Show the schedule for each teacher

foreach my $teacher (@teachers) {
    printf("\nSchedule for teacher %s\n\n",$teacher);
    printf("    %-25s %-25s %-25s\n","Monday","Tuesday","Wednesday");
    foreach my $hour (@hours) {
	printf("%2d: ",$hour);
	foreach my $day (@days) {
	    $s = "";
	    foreach my $class (@classes) {
		foreach my $group (@groups) {
		    if((%classtime{"$class-$group-$hour"} == 1) && (%classday{"$class-$group-$day"} == 1) && ($classteacher{"$class-$group-$teacher"} == 1)) {
			$s = "$s$class/$group ";
		    }
		}
	    }
	    printf("%-24s ",$s);
	}
	printf("\n");
    }
    printf("\n");
}
