package bjp;

BEGIN { $ENV{'DANCER_ENVIRONMENT'} = 'production' }

use Dancer2;
use GenerateBJP;

our $VERSION = '1.0';

set port => "3000";


get '/' => sub {
    template 'index';
};

get '/hello/:name' => sub {
    return "Hi there " . params->{name};
};

any ['get'] => qr{^/bjp.*} => sub {
    template 'bjp.tt', { name => 'test' };
};

any ['post'] => qr{^/bjp.*} => sub {
  my $post = request->params;
  &GenerateBJP::displayBJP($post);
};

true;
