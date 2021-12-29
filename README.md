※2021/12/29追記
もっと良いコードがあります。
https://gist.github.com/Bokuchin/8050a7121f505a697e250df4d8cfbd3b
解説記事も書きました。
https://qiita.com/Bokuchin/items/0d1f81d79ff8058a729c
※追記終わり

rensha.py  
ラズパイ4モデルBで実行するコード。  
スイッチのプロコンのZRボタンを連射化。  
Lボタンを普通のZRボタンを押した時のにする。  
  
使い方は
https://github.com/Bokuchin/SwitchProconGyroMouse
こちらのmouse_gyro.pyの実行法と同じです。  
Qiita記事にmouse_gyro.pyを使うまでの準備方法が書いてあるので
sudo python3 mouse_gyro.pyをsudo python3 rensha.pyに変えて実行すれば使えます。  
rensha.pyではマウスは使用しないのでどんなマウスを使ってても構いません。  
rensha.pyにはmouse_gyro.pyの名残でマウスを色々する部分が残っていますが、その部分を消すかコメントアウトしてしまって構いません。
