package org.grupo1.nfc_access.fragments;

import android.app.DialogFragment;
import android.content.Context;
import android.media.MediaPlayer;
import android.nfc.FormatException;
import android.nfc.NdefMessage;
import android.nfc.NdefRecord;
import android.nfc.tech.Ndef;
import android.os.Build;
import android.os.Bundle;
import android.os.VibrationEffect;
import android.os.Vibrator;
import android.support.annotation.Nullable;
import android.support.annotation.RequiresApi;
import android.util.Log;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.ProgressBar;
import android.widget.TextView;

import org.grupo1.nfc_access.MainActivity;
import org.grupo1.nfc_access.R;

import java.io.IOException;
import java.nio.charset.Charset;

public class NFCWriteFragment extends DialogFragment {
    
    public static final String TAG = NFCWriteFragment.class.getSimpleName();

    public static NFCWriteFragment newInstance(String tag) {
        NFCWriteFragment fragment = new NFCWriteFragment();
        Bundle args = new Bundle();
        args.putString("tag", tag);
        fragment.setArguments(args);
        return fragment;
    }

    private String messageToWrite;
    private TextView mTvMessage;
    private ProgressBar mProgress;
    private Listener mListener;
    private MediaPlayer successSound;

    @Nullable
    @Override
    public View onCreateView(LayoutInflater inflater, ViewGroup container, Bundle savedInstanceState) {
        View view = inflater.inflate(R.layout.fragment_write,container,false);
        Bundle args = getArguments();
        this.messageToWrite = args.getString("tag");
        successSound = MediaPlayer.create(getActivity(), R.raw.correct);
        initViews(view);
        return view;
    }

    private void initViews(View view) {

        mTvMessage = (TextView) view.findViewById(R.id.tv_message);
        mProgress = (ProgressBar) view.findViewById(R.id.progress);
    }

    @Override
    public void onAttach(Context context) {
        super.onAttach(context);
        mListener = (MainActivity)context;
        mListener.onDialogDisplayed(true, this.messageToWrite);
    }

    @Override
    public void onDetach() {
        super.onDetach();
        mListener.onDialogDismissed();
    }

    public void onNfcDetected(Ndef ndef, String messageToWrite){
        mProgress.setVisibility(View.VISIBLE);
        writeToNfc(ndef,messageToWrite);
    }

    private void writeToNfc(Ndef ndef, String message){

        mTvMessage.setText(getString(R.string.message_write_progress));
        if (ndef != null) {

            try {
                ndef.connect();
                NdefRecord mimeRecord = NdefRecord.createMime("text/plain", message.getBytes(Charset.forName("US-ASCII")));
                ndef.writeNdefMessage(new NdefMessage(mimeRecord));
                ndef.close();
                //Write Successful
                successSound.start();
                if (Build.VERSION.SDK_INT >= 26) {
                    createOneShotVibrationUsingVibrationEffect();
                }else {
                    vibrate();
                }
                mTvMessage.setText(getString(R.string.message_write_success));

            } catch (IOException | FormatException e) {
                e.printStackTrace();
                mTvMessage.setText(getString(R.string.message_write_error));

            } finally {
                mProgress.setVisibility(View.GONE);
            }

        }
    }

    private void vibrate() {
        Vibrator mVibrator = (Vibrator) getActivity().getSystemService(Context.VIBRATOR_SERVICE);
        mVibrator.vibrate(200);
    }

    @RequiresApi(api = 26)
    private void createOneShotVibrationUsingVibrationEffect() {
        Vibrator mVibrator = (Vibrator) getActivity().getSystemService(Context.VIBRATOR_SERVICE);
        VibrationEffect effect = VibrationEffect.createOneShot(200, VibrationEffect.DEFAULT_AMPLITUDE);
        mVibrator.vibrate(effect);
    }
}
