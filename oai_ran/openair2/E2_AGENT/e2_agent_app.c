//
// Created by root on 6/30/22.
//

#include "e2_agent_app.h"

#include <common/utils/system.h>

#include <pthread.h>
#include <arpa/inet.h>

#include "common/ran_context.h"
#include "common/utils/LOG/log.h"
#include "e2_message_handlers.h"
#include "intertask_interface.h"

extern RAN_CONTEXT_t RC;


int agent_task_created = 0;
pthread_t heartbeat_thread; // heartbeat has a mutex to easily stop heartbeat messages if needed (just lock the mutex)
e2_agent_databank_t* e2_agent_db = NULL;

int e2_agent_init(){
    e2_agent_info_t* agent_info = malloc(sizeof(e2_agent_info_t));
    LOG_D(E2_AGENT,"Initializing E2 agent\n");

    // heartbeat thread and mutex init
    if(pthread_create(&heartbeat_thread,NULL,&e2_heartbeat, agent_info)) {
        LOG_E(E2_AGENT, "Could not init heartbeat thread\n");
        return -1;
    }
    pthread_detach(heartbeat_thread);

    if (pthread_mutex_init(&(agent_info->hb_mutex), NULL) != 0)
    {
        LOG_E(E2_AGENT,"Could not init mutex\n");
        return -1;
    }
    // network init
    // create sockets
    // if((agent_info->in_sockfd = socket(AF_INET, SOCK_DGRAM, 0)) < 0){
    //     perror("Failed to create in socket\n");
    //     exit(EXIT_FAILURE);
    // }
    if((agent_info->listen_sockfd = socket(AF_INET, SOCK_STREAM, 0)) < 0){
        perror("Failed to create TCP socket\n");
        exit(EXIT_FAILURE);
    }

    // setsockopt(agent_info->in_sockfd, SOL_SOCKET, SO_REUSEADDR, &(agent_info->reuse), sizeof(agent_info->reuse));
    setsockopt(agent_info->listen_sockfd, SOL_SOCKET, SO_REUSEADDR, &(agent_info->reuse), sizeof(agent_info->reuse));
    memset(&(agent_info->server_sockaddr), 0, sizeof(agent_info->server_sockaddr));

    // if((agent_info->out_sockfd = socket(AF_INET, SOCK_DGRAM, 0)) < 0){
    //     perror("Failed to create out socket\n");
    //     exit(EXIT_FAILURE);
    // }
    // memset(&(agent_info->out_sockaddr), 0, sizeof(agent_info->out_sockaddr));
    // memset(&(agent_info->in_sockaddr), 0, sizeof(agent_info->in_sockaddr));

    // agent_info->out_sockaddr.sin_family = AF_INET;
    // char ip_address[] = "127.0.0.1";
    // agent_info->out_sockaddr.sin_addr.s_addr = inet_addr(ip_address);
    // // agent_info->out_sockaddr.sin_addr.s_addr = INADDR_ANY;
    // agent_info->out_sockaddr.sin_port = htons(E2AGENT_OUT_PORT);

    // agent_info->in_sockaddr.sin_family = AF_INET;
    // agent_info->in_sockaddr.sin_addr.s_addr = INADDR_ANY;
    // agent_info->in_sockaddr.sin_port = htons(E2AGENT_IN_PORT);

    agent_info->server_sockaddr.sin_family = AF_INET;
    agent_info->server_sockaddr.sin_addr.s_addr = INADDR_ANY;
    agent_info->server_sockaddr.sin_port = htons(6600);
    // Bind socket
    if (bind(agent_info->listen_sockfd, (struct sockaddr *) &(agent_info->server_sockaddr), sizeof(agent_info->server_sockaddr)) != 0) {
        perror("Failed to bind listen socket");
        exit(EXIT_FAILURE);
    }
    // Listen cho connection từ client
    if (listen(agent_info->listen_sockfd, 5) < 0) {
        perror("Failed to listen");
        exit(EXIT_FAILURE);
    }
    LOG_I(E2_AGENT, "TCP server listening on port 6600...\n");

    LOG_D(E2_AGENT, "Initializing data bank\n");
    e2_agent_db = malloc(sizeof(e2_agent_databank_t));
    if (pthread_mutex_init(&(e2_agent_db->mutex), NULL) != 0)
    {
        LOG_E(E2_AGENT,"Could not init db mutex\n");
        return -1;
    }
    e2_agent_db->max_prb = -1;
    e2_agent_db->true_gbr = 0;


    // if (bind(agent_info->in_sockfd, (struct sockaddr *) &(agent_info->in_sockaddr), sizeof(agent_info->in_sockaddr)) != 0) {
    //     perror("Failed to bind in socket");
    //     exit(EXIT_FAILURE);
    // }
    // LOG_D(E2_AGENT, "Agent waiting for UDP datagrams\n");

    // Properly wrapping agent_info in an ittiTask_parms_t structure
    ittiTask_parms_t task_params;
    task_params.args_to_start_routine = agent_info;   // Directly pass agent_info
    task_params.shortcut_func = NULL;

    // create itti task
    if(itti_create_task(TASK_E2_AGENT,e2_agent_task, &task_params) < 0){
        LOG_E(E2_AGENT, "cannot create ITTI task\n");
        return -1;
    }
    return 0;
}

void* e2_heartbeat(void* args) {
    // this is mutex protected such that heartbeats can be stopped anytime by locking the mutex sw else
    INFINITE_LOOP{
        pthread_mutex_lock(&((e2_agent_info_t*) args)->hb_mutex);
        LOG_I(E2_AGENT, "E2 agent heartbeat\n\n");
        pthread_mutex_unlock(&((e2_agent_info_t*) args)->hb_mutex);
        sleep(3);
    }
}


void* e2_handle_client(void* args) {
    e2_client_info_t* client_info = (e2_client_info_t*)args;
    uint8_t recv_buf[E2AGENT_MAX_BUF_SIZE];

    LOG_I(E2_AGENT, "New client thread: %s:%d\n",
          inet_ntoa(client_info->client_addr.sin_addr),
          ntohs(client_info->client_addr.sin_port));

    while (1) {
        int rcv_len = recv(client_info->sockfd, recv_buf, E2AGENT_MAX_BUF_SIZE, 0);
        if (rcv_len <= 0) {
            LOG_I(E2_AGENT, "Client disconnected: %s:%d\n",
                  inet_ntoa(client_info->client_addr.sin_addr),
                  ntohs(client_info->client_addr.sin_port));
            break;
        }
        LOG_D(E2_AGENT, "Received %d bytes from client\n", rcv_len);
        handle_master_message(recv_buf, rcv_len, client_info->sockfd);
    }

    close(client_info->sockfd);
    free(client_info);
    return NULL;
}

void *e2_agent_task(void* args_p){
    e2_agent_info_t* e2_info = args_p;
    uint8_t recv_buf[E2AGENT_MAX_BUF_SIZE];
    int rcv_len;
    unsigned slen;
    slen = sizeof(e2_info->in_sockaddr);
    itti_mark_task_ready(TASK_E2_AGENT);

    struct sockaddr_in client_addr;
    socklen_t addr_len = sizeof(client_addr);
    while (1) {
        int conn_sockfd = accept(e2_info->listen_sockfd, (struct sockaddr*)&client_addr, &addr_len);
        if (conn_sockfd < 0) {
            perror("Failed to accept connection");
            continue;
        }

        LOG_I(E2_AGENT, "Accepted connection from %s:%d\n",
              inet_ntoa(client_addr.sin_addr), ntohs(client_addr.sin_port));

        // Tạo thông tin client
        e2_client_info_t* client_info = malloc(sizeof(e2_client_info_t));
        client_info->sockfd = conn_sockfd;
        client_info->client_addr = client_addr;

        // Tạo thread mới xử lý client
        pthread_t client_thread;
        if (pthread_create(&client_thread, NULL, e2_handle_client, client_info) != 0) {
            perror("Failed to create thread for client");
            close(conn_sockfd);
            free(client_info);
            continue;
        }

        pthread_detach(client_thread);  // Không cần join
    }

    // INFINITE_LOOP {
    //     /* Wait for a client */
    //     rcv_len = recvfrom(e2_info->in_sockfd, recv_buf, E2AGENT_MAX_BUF_SIZE, 0, (struct sockaddr *) &(e2_info->in_sockaddr), &slen);
    //     LOG_D(E2_AGENT, "Received %d bytes\n", rcv_len);
    //     handle_master_message(recv_buf, rcv_len, e2_info->out_sockfd, e2_info->out_sockaddr);
    // }

}
