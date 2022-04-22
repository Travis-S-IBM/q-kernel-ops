# shared kernel metadata

## Mounting the Linode NFS share 

### on Linux

```sh
mount -t nfs 45.33.80.108:/home/nfs <full pathname to q-kernel-ops>/resources/shared_kernel_metadata
```

### on MacOS

see and test https://www.wdiaz.org/how-to-mount-nfs-share-on-mac/

## ToDO

### Explore alternatives

 - if the latency on the free (for now) Linode share is too high, we can switch to a an IBM cloud share 
 - mind that this will eat into our $200.00 credit on IBM Cloud as it is not free.  
 - another alternative would be to continue to do storage on github since we seem to have a lot less time for each run that necessarily limits how large these files will get
