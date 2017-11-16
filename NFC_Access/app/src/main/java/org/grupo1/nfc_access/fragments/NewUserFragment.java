package org.grupo1.nfc_access.fragments;

import android.os.Bundle;
import android.support.design.widget.FloatingActionButton;
import android.support.v4.app.Fragment;
import android.util.Log;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;

import com.android.volley.Request;
import com.android.volley.Response;
import com.android.volley.VolleyError;
import com.android.volley.toolbox.JsonObjectRequest;

import org.grupo1.nfc_access.R;
import org.grupo1.nfc_access.utils.HTTPHandler;
import org.json.JSONObject;

/**
 * A simple {@link Fragment} subclass.
 * Use the {@link NewUserFragment#newInstance} factory method to
 * create an instance of this fragment.
 */
public class NewUserFragment extends Fragment{

    public static final String TAG = NFCWriteFragment.class.getSimpleName();

    private FloatingActionButton mBtWrite;

    private NFCWriteFragment mNfcWriteFragment;

    String url = "http://www.google.com";

    public NewUserFragment() {
        // Required empty public constructor
    }

    /**
     * Use this factory method to create a new instance of
     * this fragment using the provided parameters.
     *
     * @return A new instance of fragment NewUserFragment.
     */
    // TODO: Rename and change types and number of parameters
    public static NewUserFragment newInstance() {
        NewUserFragment fragment = new NewUserFragment();
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
        View v = inflater.inflate(R.layout.fragment_new_user, container, false);
        mBtWrite = v.findViewById(R.id.btn_write);

        mBtWrite.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                createNewUser();
                showWriteFragment();
            }
        });
        return v;
    }

    private void createNewUser(){
        JsonObjectRequest jsObjRequest = new JsonObjectRequest
                (Request.Method.GET, url, null, new Response.Listener<JSONObject>() {

                    @Override
                    public void onResponse(JSONObject response) {
                        Log.d(TAG,"Response: " + response.toString());
                    }
                }, new Response.ErrorListener() {

                    @Override
                    public void onErrorResponse(VolleyError error) {
                        Log.d(TAG,"ErrorResponse: " + error.toString());

                    }
                });
        HTTPHandler.getInstance(getActivity()).addToRequestQueue(jsObjRequest);
    }

    private void showWriteFragment() {

        mNfcWriteFragment = (NFCWriteFragment) getActivity().getFragmentManager().findFragmentByTag(NFCWriteFragment.TAG);

        if (mNfcWriteFragment == null) {

            mNfcWriteFragment = NFCWriteFragment.newInstance();
        }
        mNfcWriteFragment.show(getActivity().getFragmentManager(),NFCWriteFragment.TAG);

    }
}
