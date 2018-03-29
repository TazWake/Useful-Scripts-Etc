<?php
/* example password generator */

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
