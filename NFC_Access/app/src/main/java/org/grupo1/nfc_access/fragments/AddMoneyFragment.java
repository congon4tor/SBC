package org.grupo1.nfc_access.fragments;

import android.os.Bundle;
import android.support.design.widget.FloatingActionButton;
import android.support.v4.app.Fragment;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;

import org.grupo1.nfc_access.R;

/**
 * A simple {@link Fragment} subclass.
 * Use the {@link AddMoneyFragment#newInstance} factory method to
 * create an instance of this fragment.
 */
public class AddMoneyFragment extends Fragment {

    public static final String TAG = NFCReadFragment.class.getSimpleName();

    private NFCReadFragment mNfcReadFragment;

    private FloatingActionButton mBtNFC;
    private FloatingActionButton mBtSend;


    public AddMoneyFragment() {
        // Required empty public constructor
    }

    /**
     * Use this factory method to create a new instance of
     * this fragment using the provided parameters.
     *
     * @return A new instance of fragment AddMoneyFragment.
     */
    public static AddMoneyFragment newInstance() {
        AddMoneyFragment fragment = new AddMoneyFragment();
        return fragment;
    }

    @Override
    public void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
    }

    @Override
    public View onCreateView(LayoutInflater inflater, ViewGroup container,
                             Bundle savedInstanceState) {
        // Inflate the layout for this fragment
        View v = inflater.inflate(R.layout.fragment_add_money, container, false);

        mBtNFC = v.findViewById(R.id.btn_nfc);
        mBtSend = v.findViewById(R.id.btn_send);

        mBtNFC.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                showReadFragment();
            }
        });
        mBtSend.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                showReadFragment();
            }
        });

        showReadFragment();
        return v;
    }

    private void showReadFragment() {

        mNfcReadFragment =  (NFCReadFragment) getActivity().getFragmentManager().findFragmentByTag(NFCReadFragment.TAG);

        if (mNfcReadFragment == null) {

            mNfcReadFragment = NFCReadFragment.newInstance();
        }
        mNfcReadFragment.show(getActivity().getFragmentManager(),NFCReadFragment.TAG);

    }
}
