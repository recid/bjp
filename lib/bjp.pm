package bjp;
use Dancer2;

our $VERSION = '0.1';

get '/' => sub {
    template 'index';
};

get '/hello/:name' => sub {
    return "Hi there " . params->{name};
};

any ['get', 'post'] => qr{^/bjp.*} => sub {
    template 'bjp.tt', { name => 'test' };
};

true;
