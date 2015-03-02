package bjp;
use Dancer2;
use GenerateBJP;

our $VERSION = '0.1';

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
