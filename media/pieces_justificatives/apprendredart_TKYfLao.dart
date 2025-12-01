void main(){
  int nombre = 4;
  List <String> ville=['kinshasa','libreville'];
  print('hello world $nombre $ville');
  ville.add('katanga');
  print(ville);
  dynamic nom='benjamin';
  nom=12;
  print(nom);
  Map capital={
    'congo':'kinshasa',
    'la chine':'pekin',
    'gabon':'libreville'
  };
  print( capital.length);

  capital.forEach((pays,capit){
   print('la capitale de $pays est $capit');
  });
  var dates= DateTime.now();
  print('La date: $dates');
}