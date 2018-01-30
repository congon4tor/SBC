/**
 * Para compilar: gcc -o test test.c -lcurl -ljson-c
 * el -lcurl linkea nuestro programa a la lib curl
 * 
 **/


#include <stdio.h>
#include <curl/curl.h>
#include <json-c/json.h>


void tryAccess(size_t (*callback)(void*,size_t,size_t,void*),char cod_uid[]){

  CURL *curl;
  CURLcode res;

  json_object *json;      /* json post body */
 
  /* In windows, this will init the winsock stuff */ 
  curl_global_init(CURL_GLOBAL_ALL);
 
  /* get a curl handle */ 
  curl = curl_easy_init();
  if(curl) {

    /* create json object for post */
    json = json_object_new_object();

    /* build post data */
    json_object_object_add(json, "TAG", json_object_new_string(cod_uid));
    json_object_object_add(json, "ID_Sala", json_object_new_string("5"));

    struct curl_slist *headers = NULL;
    headers = curl_slist_append(headers, "Accept: application/json");
    headers = curl_slist_append(headers, "Content-Type: application/json");
    headers = curl_slist_append(headers, "charsets: utf-8");

    curl_easy_setopt(curl, CURLOPT_URL, "http://192.168.0.113:5000/tryAccess");
    curl_easy_setopt(curl, CURLOPT_HTTPHEADER, headers);
    /* Now specify the POST data */ 
    curl_easy_setopt(curl, CURLOPT_POSTFIELDS, json_object_to_json_string(json));
    curl_easy_setopt(curl, CURLOPT_WRITEFUNCTION, callback);
 
    /* Perform the request, res will get the return code */ 
    res = curl_easy_perform(curl);
    /* Check for errors */ 
    if(res != CURLE_OK)
      fprintf(stderr, "curl_easy_perform() failed: %s\n",
              curl_easy_strerror(res));
    
    
    /* always cleanup */ 
    curl_easy_cleanup(curl);

    /* free headers */
    curl_slist_free_all(headers);

    /* free json object */
    json_object_put(json);

  }
  curl_global_cleanup();
}

void exitRoom(size_t (*callback)(void*,size_t,size_t,void*)){

  CURL *curl;
  CURLcode res;

  json_object *json;      /* json post body */
 
  /* In windows, this will init the winsock stuff */ 
  curl_global_init(CURL_GLOBAL_ALL);
 
  /* get a curl handle */ 
  curl = curl_easy_init();
  if(curl) {

    /* create json object for post */
    json = json_object_new_object();

    /* build post data */
    json_object_object_add(json, "TAG", json_object_new_string("F2 50 CB A9"));
    json_object_object_add(json, "ID_Sala", json_object_new_string("5"));

    struct curl_slist *headers = NULL;
    headers = curl_slist_append(headers, "Accept: application/json");
    headers = curl_slist_append(headers, "Content-Type: application/json");
    headers = curl_slist_append(headers, "charsets: utf-8");

    curl_easy_setopt(curl, CURLOPT_URL, "http://192.168.0.113:5000/exitRoom");
    curl_easy_setopt(curl, CURLOPT_HTTPHEADER, headers);
    /* Now specify the POST data */ 
    curl_easy_setopt(curl, CURLOPT_POSTFIELDS, json_object_to_json_string(json));
    curl_easy_setopt(curl, CURLOPT_WRITEFUNCTION, callback);
 
    /* Perform the request, res will get the return code */ 
    res = curl_easy_perform(curl);
    /* Check for errors */ 
    if(res != CURLE_OK)
      fprintf(stderr, "curl_easy_perform() failed: %s\n",
              curl_easy_strerror(res));
    
    
    /* always cleanup */ 
    curl_easy_cleanup(curl);

    /* free headers */
    curl_slist_free_all(headers);

    /* free json object */
    json_object_put(json);

  }
  curl_global_cleanup();
}

void getRoomData(size_t (*callback)(void*,size_t,size_t,void*)){

  CURL *curl;
  CURLcode res;

  json_object *json;      /* json post body */
 
  /* In windows, this will init the winsock stuff */ 
  curl_global_init(CURL_GLOBAL_ALL);
 
  /* get a curl handle */ 
  curl = curl_easy_init();
  if(curl) {

    /* create json object for post */
    json = json_object_new_object();

    /* build post data */
    json_object_object_add(json, "ID_Sala", json_object_new_string("5"));

    struct curl_slist *headers = NULL;
    headers = curl_slist_append(headers, "Accept: application/json");
    headers = curl_slist_append(headers, "Content-Type: application/json");
    headers = curl_slist_append(headers, "charsets: utf-8");

    curl_easy_setopt(curl, CURLOPT_URL, "http://192.168.0.113:5000/getRoomData");
    curl_easy_setopt(curl, CURLOPT_HTTPHEADER, headers);
    /* Now specify the POST data */ 
    curl_easy_setopt(curl, CURLOPT_POSTFIELDS, json_object_to_json_string(json));
    curl_easy_setopt(curl, CURLOPT_WRITEFUNCTION, callback);
 
    /* Perform the request, res will get the return code */ 
    res = curl_easy_perform(curl);
    /* Check for errors */ 
    if(res != CURLE_OK)
      fprintf(stderr, "curl_easy_perform() failed: %s\n",
              curl_easy_strerror(res));
    
    
    /* always cleanup */ 
    curl_easy_cleanup(curl);

    /* free headers */
    curl_slist_free_all(headers);

    /* free json object */
    json_object_put(json);

  }
  curl_global_cleanup();
}