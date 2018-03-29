<?php
/* example password generator */

/*
=============================================
== This should be saved as a separate file ==
=============================================
*/
namespace Application\Security;
class PassGen
{
  const SOURCE_SUFFIX = 'src';
  const SPECIAL_CHARS = 
    '\`¬|!"£$%^&*()_-+={}[]:@~;\'#<>?,./|\\';
  protected $algorithm;
  protected $sourceList;
  protected $word;
  protected $list;
  
  public function digits($max = 999)
{
  return random_int(1, $max);
}

public function special()
{
  $maxSpecial = strlen(self::SPECIAL_CHARS) - 1;
  return self::SPECIAL_CHARS[random_int(0, $maxSpecial)];
}
if (!file_exists($sourceFile) || filesize($sourceFile) == 0) {
    echo 'Processing: ' . $html . PHP_EOL;
    $contents = file_get_contents($html);
    if (preg_match('/<body>(.*)<\/body>/i', 
        $contents, $matches)) {
        $contents = $matches[1];
    }
    $list = str_word_count(strip_tags($contents), 1);
    foreach ($list as $key => $value) {
       if (strlen($value) < $minWordLength) {
         $list[$key] = 'xxxxxx';
       } else {
         $list[$key] = trim($value);
       }
     }
     $list = array_unique($list);
     file_put_contents($sourceFile, implode("\n",$list));
   }
  }
  return TRUE;
}
public function flipUpper($word)
{
  $maxLen   = strlen($word);
  $numFlips = random_int(1, $maxLen - 1);
  $flipped  = strtolower($word);
  for ($x = 0; $x < $numFlips; $x++) {
       $pos = random_int(0, $maxLen - 1);
       $word[$pos] = strtoupper($word[$pos]);
  }
  return $word;
}
public function word()
{
  $wsKey    = random_int(0, count($this->sourceList) - 1);
  $list     = file($this->sourceList[$wsKey]);
  $maxList  = count($list) - 1;
  $key      = random_int(0, $maxList);
  $word     = $list[$key];
  return $this->flipUpper($word);
}
public function initAlgorithm()
{
  $this->algorithm = [
    ['word', 'digits', 'word', 'special'],
    ['digits', 'word', 'special', 'word'],
    ['word', 'word', 'special', 'digits'],
    ['special', 'word', 'special', 'digits'],
    ['word', 'special', 'digits', 'word', 'special'],
    ['special', 'word', 'special', 'digits', 
    'special', 'word', 'special'],
  ];
}
public function __construct(
  array $wordSource, $minWordLength, $cacheDir)
{
  $this->processSource($wordSource, $minWordLength, $cacheDir);
  $this->initAlgorithm();
}
public function generate()
{
  $pwd = '';
  $key = random_int(0, count($this->algorithm) - 1);
  foreach ($this->algorithm[$key] as $method) {
    $pwd .= $this->$method();
  }
  return str_replace("\n", '', $pwd);
}

}
?>
