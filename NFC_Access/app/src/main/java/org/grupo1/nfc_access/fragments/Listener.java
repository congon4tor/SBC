package org.grupo1.nfc_access.fragments;

public interface Listener {

    void onDialogDisplayed(boolean isWrite, String messageToWrite);

    void onDialogDismissed();
}
