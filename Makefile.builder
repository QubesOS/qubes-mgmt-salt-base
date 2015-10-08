# vim: filetype=make

ifndef LOADING_PLUGINS
    SOURCE_COPY_IN := source-mgmt-salt-base-copy-in
    _rpm_spec_files := rpm_spec/qubes-mgmt-salt-base.spec
    
    ifeq ($(PACKAGE_SET),dom0)
            RPM_SPEC_FILES := $(_rpm_spec_files)

    else ifeq ($(PACKAGE_SET),vm)
        ifneq ($(filter $(DISTRIBUTION), debian qubuntu),)
            DEBIAN_BUILD_DIRS := debian
	else
            RPM_SPEC_FILES := $(_rpm_spec_files)
        endif
    endif
endif

# mgmt-salt's Makefile.builder will copy a shared Makefile.install to the
# chroot environment and parse and dump the yaml FORMULA configuration
# file to Makefile.vars in the chroot environment as well.
#
# mgmt-salt also contains the shared copy-in function
source-mgmt-salt-base-copy-in:
	@$(call MGMT_INSTALL_MAKEFILES) 
	@$(call MGMT_COPY_IN)
