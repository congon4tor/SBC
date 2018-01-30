package org.grupo1.nfc_access.fragments;

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
import com.android.volley.toolbox.StringRequest;

import org.grupo1.nfc_access.MainActivity;
import org.grupo1.nfc_access.R;
import org.grupo1.nfc_access.utils.HTTPHandler;
import org.json.JSONException;
import org.json.JSONObject;

/**
 * A simple {@link Fragment} subclass.
 * Use the {@link NewUserFragment#newInstance} factory method to
 * create an instance of this fragment.
 */
public class NewUserFragment extends Fragment{

    public static final String TAG = NewUserFragment.class.getSimpleName();

    private FloatingActionButton mBtWrite;
    private EditText mNombreEditText;
    private EditText mApellidosEditText;
    private EditText mDNIEditText;
    private EditText mNivelEditText;

    private NFCReadFragment mNfcReadFragment;

    public NewUserFragment() {
        // Required empty public constructor
    }

    /**
     * Use this factory method to create a new instance of
     * this fragment using the provided parameters.
     *
     * @return A new instance of fragment NewUserFragment.
     */
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
        mNombreEditText = v.findViewById(R.id.name);
        mApellidosEditText = v.findViewById(R.id.lastname);
        mDNIEditText = v.findViewById(R.id.DNI);
        mNivelEditText = v.findViewById(R.id.accessLevel);

        ((MainActivity)getActivity()).passVal(new FragmentCommunicator() {

            @Override
            public void passTag(String tag) {
                createNewUser(mDNIEditText.getText().toString(), mNombreEditText.getText().toString(),mApellidosEditText.getText().toString(),mNivelEditText.getText().toString(),tag);

            }
        });

        mBtWrite.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                showReadFragment();
            }
        });
        return v;
    }

    private String createNewUser(String dni, String nombre, String apellidos, String nivel, String tag){
        JSONObject jsonObj = new JSONObject();
        try {
            jsonObj.put("DNI", dni);
            jsonObj.put("Nombre", nombre);
            jsonObj.put("Apellidos", apellidos);
            jsonObj.put("Nivel_Acceso", nivel);
            jsonObj.put("tag", tag);

            JsonObjectRequest jsObjRequest = new JsonObjectRequest
                    (Request.Method.POST, getResources().getString(R.string.serverhost)+"/newUser", jsonObj, new Response.Listener<JSONObject>() {

                        @Override
                        public void onResponse(JSONObject response) {
                            Log.d(TAG,"Response: " + response.toString());
                            try {
                                if(response.getString("response").equals("success")){
                                    Toast.makeText(getActivity().getApplicationContext(),R.string.asistente_añadidos_correctamente,Toast.LENGTH_LONG).show();
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
        return "";
    }

    private void showReadFragment() {

        mNfcReadFragment =  (NFCReadFragment) getActivity().getFragmentManager().findFragmentByTag(NFCReadFragment.TAG);

        if (mNfcReadFragment == null) {

            mNfcReadFragment = NFCReadFragment.newInstance();
        }
        mNfcReadFragment.show(getActivity().getFragmentManager(),NFCReadFragment.TAG);

    }
}
