package org.grupo1.nfc_access;

import android.annotation.SuppressLint;
import android.content.Intent;
import android.graphics.drawable.Animatable;
import android.graphics.drawable.AnimatedStateListDrawable;
import android.graphics.drawable.AnimatedVectorDrawable;
import android.graphics.drawable.AnimationDrawable;
import android.graphics.drawable.Drawable;
import android.media.MediaPlayer;
import android.support.annotation.Nullable;
import android.support.v7.app.ActionBar;
import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;
import android.os.Handler;
import android.view.MotionEvent;
import android.view.View;
import android.view.animation.Animation;
import android.widget.ImageView;

/**
 * An example full-screen activity that shows and hides the system UI (i.e.
 * status bar and navigation/system bar) with user interaction.
 */
public class SplashActivity extends AppCompatActivity {


    // Splash screen timer
    private static final int SPLASH_TIME_OUT = 3000;
    private static final int ANIM_TIME_OUT = 500;
    private static final int SOUND_TIME_OUT = 2000;


    private ImageView nfcImg;
    private ImageView keyImg;
    private ImageView openImg;


    private MediaPlayer unlockSound;


    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);

        setContentView(R.layout.activity_splash);


        nfcImg = (ImageView) findViewById(R.id.nfc_img);
        keyImg = (ImageView) findViewById(R.id.key_img);
        openImg = (ImageView) findViewById(R.id.open_img);

        unlockSound  = MediaPlayer.create(this, R.raw.unlock);


        //esperamos un tiempo y comenzamos la animacion
        new Handler().postDelayed(new Runnable() {

            @Override
            public void run() {

                keyImg.setVisibility(View.VISIBLE);
                nfcImg.setVisibility(View.VISIBLE);
                openImg.setVisibility(View.VISIBLE);
                Drawable drawable_key = keyImg.getDrawable();
                Drawable drawable_nfc = nfcImg.getDrawable();
                Drawable drawable_open = openImg.getDrawable();

                if(drawable_key instanceof Animatable){
                    ((Animatable) drawable_key).start();
                }
                if(drawable_nfc instanceof Animatable){
                    ((Animatable) drawable_nfc).start();
                }
                if(drawable_open instanceof Animatable){
                    ((Animatable) drawable_open).start();
                }
            }
        }, ANIM_TIME_OUT);

        //esperamos un tiempo y reproducimos el sonido de la animacion
        new Handler().postDelayed(new Runnable() {

            @Override
            public void run() {
                unlockSound.start();
            }
        }, SOUND_TIME_OUT);

        //esperamos un tiempo y pasamos a la actividad main
        new Handler().postDelayed(new Runnable() {

            @Override
            public void run() {

                Intent i = new Intent(SplashActivity.this, MainActivity.class);
                startActivity(i);

                // Acabar esta actividad
                finish();
            }
        }, SPLASH_TIME_OUT);

    }
}
