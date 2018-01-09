package org.grupo1.nfc_access.fragments;

import android.bluetooth.le.PeriodicAdvertisingParameters;
import android.os.Bundle;
import android.support.design.widget.FloatingActionButton;
import android.support.v4.app.Fragment;
import android.util.Log;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.EditText;
import android.widget.Toast;

import com.android.volley.Request;
import com.android.volley.Response;
import com.android.volley.VolleyError;
import com.android.volley.toolbox.JsonObjectRequest;

import org.grupo1.nfc_access.MainActivity;
import org.grupo1.nfc_access.R;
import org.grupo1.nfc_access.utils.HTTPHandler;
import org.json.JSONException;
import org.json.JSONObject;

/**
 * A simple {@link Fragment} subclass.
 * Use the {@link PaymentFragment#newInstance} factory method to
 * create an instance of this fragment.
 */
public class PaymentFragment extends Fragment{

    public static final String TAG = PaymentFragment.class.getSimpleName();

    private NFCReadFragment mNfcReadFragment;

    private FloatingActionButton mBtNFC;
    private FloatingActionButton mBtSend;
    public FloatingActionButton mBtAdd;
    private FloatingActionButton mBtSub;
    private EditText moneyEditText;
    private EditText nameEditText;
    private EditText lastnameEditText;
    private EditText dniEditText;
    private EditText currentMoneyEditText;
    private String idAsistente;
    private int creditos;
    private int moneyToPay;


    public PaymentFragment() {
        // Required empty public constructor
    }

    /**
     * Use this factory method to create a new instance of
     * this fragment using the provided parameters.
     *
     * @return A new instance of fragment AddMoneyFragment.
     */
    public static PaymentFragment newInstance() {
        PaymentFragment fragment = new PaymentFragment();
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
        View v = inflater.inflate(R.layout.fragment_payment, container, false);

        ((MainActivity)getActivity()).passVal(new FragmentCommunicator() {

            @Override
            public void passTag(String tag) {
                loadUser(tag);
            }
        });

        mBtNFC = v.findViewById(R.id.btn_nfc);
        mBtSend = v.findViewById(R.id.btn_send);
        mBtAdd = v.findViewById(R.id.btn_more);
        mBtSub = v.findViewById(R.id.btn_less);
        moneyEditText = v.findViewById(R.id.payMoney);
        nameEditText = v.findViewById(R.id.name);
        lastnameEditText = v.findViewById(R.id.lastname);
        dniEditText = v.findViewById(R.id.DNI);
        currentMoneyEditText = v.findViewById(R.id.money);

        moneyToPay = 0;
        moneyEditText.setText(Integer.toString(moneyToPay));

        mBtNFC.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                showReadFragment();
            }
        });
        mBtSend.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                if(creditos>=moneyToPay){
                    updateMoneyAmount();
                }else {
                    Toast.makeText(getActivity().getApplicationContext(),R.string.creditos_insuficientes,Toast.LENGTH_SHORT).show();
                }

            }
        });
        mBtAdd.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                moneyToPay = getMoneyAmount();
                if(moneyToPay>=995){
                    moneyToPay=999;
                    moneyEditText.setText(Integer.toString(moneyToPay));
                }else{
                    moneyToPay += 5;
                    moneyEditText.setText(Integer.toString(moneyToPay));
                }
            }
        });
        mBtSub.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                moneyToPay = getMoneyAmount();
                if(moneyToPay>=5){
                    moneyToPay -= 5;
                    moneyEditText.setText(Integer.toString(moneyToPay));
                }else{
                    moneyToPay =0;
                    moneyEditText.setText(Integer.toString(moneyToPay));
                }


            }
        });

        showReadFragment();
        return v;
    }

    private void updateMoneyAmount(){
        if(idAsistente!=null){
            JSONObject jsonObj = new JSONObject();
            try {
                jsonObj.put("ID_Asistente", idAsistente);
                jsonObj.put("creditos", creditos-moneyToPay);
                jsonObj.put("modo_pago", 1);
                jsonObj.put("movimiento", moneyToPay);
                Log.d(TAG,jsonObj.toString());

                JsonObjectRequest jsObjRequest = new JsonObjectRequest
                        (Request.Method.POST, getResources().getString(R.string.serverhost)+"/setMoney", jsonObj, new Response.Listener<JSONObject>() {

                            @Override
                            public void onResponse(JSONObject response) {
                                Log.d(TAG,"Response: " + response.toString());
                                try {
                                    if(response.getString("response").equals("success")){
                                        currentMoneyEditText.setText(Integer.toString(creditos-moneyToPay));
                                        Toast.makeText(getActivity().getApplicationContext(),R.string.creditos_pagados_correctamente,Toast.LENGTH_LONG).show();
                                    }
                                } catch (JSONException e) {
                                    e.printStackTrace();
                                }
                            }
                        }, new Response.ErrorListener() {

                            @Override
                            public void onErrorResponse(VolleyError error) {
                                Log.d(TAG,"ErrorResponse: " + error.toString());

                            }
                        });
                HTTPHandler.getInstance(getActivity()).addToRequestQueue(jsObjRequest);
            } catch (JSONException e) {
                e.printStackTrace();
            }
        }
    }

    private void showReadFragment() {

        mNfcReadFragment =  (NFCReadFragment) getActivity().getFragmentManager().findFragmentByTag(NFCReadFragment.TAG);

        if (mNfcReadFragment == null) {

            mNfcReadFragment = NFCReadFragment.newInstance();
        }
        mNfcReadFragment.show(getActivity().getFragmentManager(),NFCReadFragment.TAG);

    }

    private int getMoneyAmount(){
        return (Integer.parseInt(moneyEditText.getText().toString()) != 0) ? Integer.parseInt(moneyEditText.getText().toString()) : 0  ;
    }

    private void loadUser(String tag){
        JSONObject jsonObj = new JSONObject();
        try {
            jsonObj.put("TAG", tag);

            JsonObjectRequest jsObjRequest = new JsonObjectRequest
                    (Request.Method.POST, getResources().getString(R.string.serverhost)+"/findUser", jsonObj, new Response.Listener<JSONObject>() {

                        @Override
                        public void onResponse(JSONObject response) {
                            Log.d(TAG,"Response: " + response.toString());
                            try {
                                if(response.getString("response").equals("success")){
                                    String data = response.getString("data");
                                    JSONObject json = new JSONObject(data);
                                    nameEditText.setText(json.getString("Nombre"));
                                    lastnameEditText.setText(json.getString("Apellidos"));
                                    dniEditText.setText(json.getString("DNI"));
                                    currentMoneyEditText.setText(Integer.toString(json.getInt("Creditos")));
                                    creditos = json.getInt("Creditos");
                                    idAsistente = json.getString("ID_Asistente");
                                }
                            } catch (JSONException e) {
                                e.printStackTrace();
                            }
                        }
                    }, new Response.ErrorListener() {

                        @Override
                        public void onErrorResponse(VolleyError error) {
                            Log.d(TAG,"ErrorResponse: " + error.toString());

                        }
                    });
            HTTPHandler.getInstance(getActivity()).addToRequestQueue(jsObjRequest);
        } catch (JSONException e) {
            e.printStackTrace();
        }
    }
}
