package org.grupo1.nfc_access.fragments;

import android.os.Bundle;
import android.support.design.widget.FloatingActionButton;
import android.support.v4.app.Fragment;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.EditText;

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
    private FloatingActionButton mBtAdd;
    private FloatingActionButton mBtSub;
    private EditText moneyEditText;
    private int moneyToAdd;


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
        mBtAdd = v.findViewById(R.id.btn_more);
        mBtSub = v.findViewById(R.id.btn_less);
        moneyEditText = v.findViewById(R.id.addMoney);

        moneyToAdd = 0;
        moneyEditText.setText(Integer.toString(moneyToAdd));

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
        mBtAdd.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                moneyToAdd = getMoneyAmount();
                if(moneyToAdd>=995){
                    moneyToAdd=999;
                    moneyEditText.setText(Integer.toString(moneyToAdd));
                }else{
                    moneyToAdd += 5;
                    moneyEditText.setText(Integer.toString(moneyToAdd));
                }
            }
        });
        mBtSub.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                moneyToAdd = getMoneyAmount();
                if(moneyToAdd>=5){
                    moneyToAdd -= 5;
                    moneyEditText.setText(Integer.toString(moneyToAdd));
                }else{
                    moneyToAdd =0;
                    moneyEditText.setText(Integer.toString(moneyToAdd));
                }


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

    public int getMoneyAmount(){
        return (Integer.parseInt(moneyEditText.getText().toString()) != 0) ? Integer.parseInt(moneyEditText.getText().toString()) : 0  ;
    }
}
