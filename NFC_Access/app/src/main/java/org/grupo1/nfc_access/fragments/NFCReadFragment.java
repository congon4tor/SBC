package org.grupo1.nfc_access.fragments;

import android.app.DialogFragment;
import android.content.Context;
import android.media.MediaPlayer;
import android.nfc.FormatException;
import android.nfc.NdefMessage;
import android.nfc.tech.Ndef;
import android.os.Build;
import android.os.Bundle;
import android.os.Parcel;
import android.os.VibrationEffect;
import android.os.Vibrator;
import android.support.annotation.Nullable;
import android.support.annotation.RequiresApi;
import android.util.Log;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.TextView;

import org.grupo1.nfc_access.MainActivity;
import org.grupo1.nfc_access.R;

import java.io.IOException;

public class NFCReadFragment extends DialogFragment {

    public static final String TAG = NFCReadFragment.class.getSimpleName();

    public static NFCReadFragment newInstance() {

        return new NFCReadFragment();
    }

    private TextView mTvMessage;
    private Listener mListener;
    private MediaPlayer successSound;

    @Nullable
    @Override
    public View onCreateView(LayoutInflater inflater, ViewGroup container, Bundle savedInstanceState) {

        View view = inflater.inflate(R.layout.fragment_read,container,false);
        successSound = MediaPlayer.create(getActivity(), R.raw.correct);
        initViews(view);
        return view;
    }

    private void initViews(View view) {

        mTvMessage = view.findViewById(R.id.tv_message);
    }

    @Override
    public void onAttach(Context context) {
        super.onAttach(context);
        mListener = (MainActivity)context;
        mListener.onDialogDisplayed(false,null);
    }

    @Override
    public void onDetach() {
        super.onDetach();
        mListener.onDialogDismissed();
    }

    public void onNfcDetected(Ndef ndef){
        readFromNFC(ndef);
    }

    private void readFromNFC(Ndef ndef) {

        try {
            ndef.connect();
            NdefMessage ndefMessage = ndef.getNdefMessage();
            String message = new String(ndefMessage.getRecords()[0].getPayload());
            successSound.start();
            if (Build.VERSION.SDK_INT >= 26) {
                createOneShotVibrationUsingVibrationEffect();
            }else {
                vibrate();
            }
            Log.d(TAG, "readFromNFC: "+message);
            mTvMessage.setText(message);
            ndef.close();

        } catch (Exception e) {
            e.printStackTrace();
            mTvMessage.setText(R.string.message_read_error);
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
