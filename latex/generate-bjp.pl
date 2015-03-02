#!/usr/bin/perl

use strict;
use warnings;


# Modules import
################################################################################

#use YAML::Tiny;
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

my $client_name = "NOMCLIENT";
my $client_address = "80 rue Roque de Fillol,
92800 Puteaux, France";
my $contact_name = "NOM_CONTACT";
my $contact_phone = "0102030405";

my $manager_name = "MON_MANAGER";
my $name = "MOI";

my $mission_name = "NOM_MISSION";
my $mission_code = "CODE_PROJET";
my $mission_description = "NATURE_MISSION";

my $year = "2015";
my $month = "1";

my $calendar = {
    6 => 'am',
    7 => 'OK',
    8 => 'OK',
    9 => 'ma',
};

my $conf = {
   client => {
     nom => $client_name,
     contact => "$contact_name / $contact_phone",
     adresse => $client_address,
   },
   linagora => {
     responsable => $manager_name,
     intervenant => $name,
   },
   mission => {
     prestation => $mission_name,
     projet => $mission_code,
     nature => $mission_description,
   },
   annee => $year,
   mois => $month,
   calendrier => $calendar,
};



&generate_conf($conf, $yaml_file);


