#!/usr/bin/perl

package GenerateBJP;

use strict;
use warnings;


# Modules import
################################################################################

use YAML::Syck;
$YAML::Syck::ImplicitTyping = 1;
$YAML::Syck::Headless = 1;



# Configuration section
################################################################################

my $yaml_file = 'bjp-test.yaml';



# Functions
################################################################################



sub generate_conf {
  my $doc = shift;
  my $file = shift;
  
  # Create a new object with a single hashref document
  #my $yaml = YAML::Tiny->new( $doc );
  
  # Save both documents to a file
  #$yaml->write( $file );
  open(my $fh, ">:encoding(UTF-8)", $file);
  DumpFile($fh, $doc);


}


# Entry point
################################################################################




#&generate_conf($conf, $yaml_file);



sub displayBJP {
  my $params = shift @_;

  my $cal = $params->{"output-half"};

  $cal =~ s/\],/|/g;      # replacing dates separators (,) by |
  $cal =~ s/[\[\]]//g;    # deleting [ and ]

  $cal =~ s/"*0\.1"*/am/g; # replace half-day notation by OK, ma, am
  $cal =~ s/"*1\.0"*/ma/g;
  $cal =~ s/"*1\.1"*/OK/g;

  # create the hash
  my %cal = map { split /,/ } split /\|/, $cal;

  # truncate the timestamp to 10 characters
  %cal = map { substr($_, 0, 10) => $cal{$_} } keys %cal; 

  # get month and year
  my $month = (localtime((keys %cal)[0]))[4] + 1;
  my $year = (localtime((keys %cal)[0]))[5] + 1900;

  # recreate the hash with the number of the day as key
  %cal = map { (localtime($_))[3] => $cal{$_} } keys %cal;

  my $calendar = \%cal;

  my $conf = {
    client => {
      nom => $params->{cname},
      contact => "$params->{ccontactname} / $params->{ccontacttel}",
      adresse => $params->{ccontactaddress},
    },
    linagora => {
      responsable => $params->{umanager},
      intervenant => $params->{uname},
    },
    mission => {
      prestation => $params->{missionname},
      projet => $params->{missioncode},
      nature => $params->{missionnature},
    },
    annee => $year,
    mois => $month,
    calendrier => $calendar,
  };

  use Data::Dumper;
  print Dumper($conf);
  print Dumper($params);
}



1;

